import contextlib
import cProfile
import importlib.util
import os
import pathlib
import threading
import time
import typing

import trustme
import uvicorn

from .models import Certificates, Pathlike

if typing.TYPE_CHECKING:
    from .config import Config  # noqa


async def app(scope: dict, receive: typing.Callable, send: typing.Callable) -> None:
    assert scope["type"] == "http"
    res = b"Hello, world"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
                [b"content-length", b"%d" % len(res)],
            ],
        }
    )
    await send({"type": "http.response.body", "body": res})


class Server(uvicorn.Server):
    def install_signal_handlers(self) -> None:
        # Disable the default installation of handlers for signals such as SIGTERM,
        # because it can only be done in the main thread.
        pass


@contextlib.contextmanager
def spawn_server(host: str, port: int, **kwargs: typing.Any) -> typing.Iterator[None]:
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        lifespan="off",
        loop="asyncio",
        log_level="warning",
        **kwargs,
    )

    server = Server(config)

    thread = threading.Thread(target=server.run)
    thread.start()

    try:
        while not server.started:
            time.sleep(1e-3)
        yield
    finally:
        server.should_exit = True
        thread.join()


CLIENT_CERT_FILENAME = "client.pem"


@contextlib.contextmanager
def generate_certificates(
    directory: Pathlike, identities: typing.Sequence[str], key_size: int = 2048,
) -> typing.Iterator[Certificates]:
    cert_dir = pathlib.Path(directory)
    cert_dir.mkdir(exist_ok=True)

    # Generate the CA certificate.
    trustme._KEY_SIZE = key_size
    ca = trustme.CA()
    cert = ca.issue_cert(*identities)

    # Write the server private key.
    server_key = cert_dir / "server.key"
    cert.private_key_pem.write_to_path(path=str(server_key))

    # Write the server certificate.
    server_cert = cert_dir / "server.pem"
    with server_cert.open(mode="w") as f:
        f.truncate()
    for blob in cert.cert_chain_pems:
        blob.write_to_path(path=str(server_cert), append=True)

    # Write the client certificate.
    client_cert = cert_dir / CLIENT_CERT_FILENAME
    ca.cert_pem.write_to_path(path=str(client_cert))

    try:
        yield Certificates(
            server_key=server_key, server_cert=server_cert, client_cert=client_cert
        )
    finally:
        os.remove(cert_dir / "server.key")
        os.remove(cert_dir / "server.pem")
        os.remove(cert_dir / CLIENT_CERT_FILENAME)


def get_client_cert(cert_dir: Pathlike) -> typing.Optional[str]:
    path = pathlib.Path(cert_dir, CLIENT_CERT_FILENAME)
    return str(path) if path.exists() else None


def load_case_entrypoint(path: str) -> typing.Callable:
    # See: https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    spec = importlib.util.spec_from_file_location("case", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    return module.main  # type: ignore


@contextlib.contextmanager
def record_profile(out: str) -> typing.Iterator[None]:
    profile = cProfile.Profile()
    profile.enable()
    yield
    profile.disable()
    profile.dump_stats(out)
