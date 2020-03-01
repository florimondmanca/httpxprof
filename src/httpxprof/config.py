import contextlib
import pathlib
import typing

import tqdm

from .utils import get_client_cert, spawn_server, generate_certificates

OUTPUT_DIR = pathlib.Path(__file__).parent / "out"
TMP_DIR = pathlib.Path(__file__).parent / "tmp"
TLS_DIR = TMP_DIR / "tls"
CASES_DIR = pathlib.Path(__file__).parent / "cases"
assert CASES_DIR.exists(), CASES_DIR


class Config:
    def __init__(self, host: str, port: int, num_requests: int, https: bool) -> None:
        self.host = host
        self.port = port
        self.num_requests = num_requests
        self.https = https

    @property
    def url(self) -> str:
        scheme = "https" if self.https else "http"
        return f"{scheme}://{self.host}:{self.port}"

    @contextlib.contextmanager
    def server(self) -> typing.Iterator[None]:
        exit_stack = contextlib.ExitStack()
        kwargs = {}

        if self.https:
            certs = exit_stack.enter_context(
                generate_certificates(directory=TLS_DIR, identities=[self.host])
            )
            kwargs["ssl_keyfile"] = str(certs.server_key)
            kwargs["ssl_certfile"] = str(certs.server_cert)

        with exit_stack, spawn_server(self.host, self.port, **kwargs):
            print(f"Server started at {self.url}")
            yield
            print("Stopping server...")

    def requests(self) -> typing.Iterator[None]:
        for _ in tqdm.tqdm(range(self.num_requests)):
            yield

    def client_cert(self) -> typing.Optional[str]:
        return get_client_cert(TLS_DIR)
