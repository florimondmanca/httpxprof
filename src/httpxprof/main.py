import asyncio
import hashlib
import os
import pathlib
import subprocess
import typing
import inspect

import click

from .config import CASES_DIR, OUTPUT_DIR, TMP_DIR, Config
from .utils import load_case_entrypoint, record_profile

CASES = [
    filename.rstrip(".py")
    for filename in os.listdir(CASES_DIR)
    if filename != "__init__.py"
]
FORMATTED_CASES = ", ".join(map(repr, CASES))


class LoadedCase(typing.NamedTuple):
    name: str
    path: pathlib.Path

    @property
    def out(self) -> pathlib.Path:
        return pathlib.Path(f"{self.name}.prof")


def name_from_script(path: pathlib.Path) -> str:
    hsh = hashlib.md5(str(path).encode()).hexdigest()
    return f"{path.stem}_{hsh}"


def handle_case(ctx: click.Context, param: click.Parameter, value: str) -> LoadedCase:
    if not value:
        raise click.BadArgumentUsage(
            f"Expected a case. Choose from {FORMATTED_CASES}, or pass a Python script."
        )

    if value.endswith(".py"):
        # Absolute case script.
        path = pathlib.Path(value)

        if not path.exists():
            raise click.BadArgumentUsage(
                f"Path to Python script {value!r} does not exist."
            )

        name = name_from_script(path)

        return LoadedCase(name=name, path=path)

    # Built-in case.
    if value not in CASES:
        raise click.BadArgumentUsage(
            f"Unknown built-in case: {value!r}. Valid options: {FORMATTED_CASES}"
        )

    name = value
    path = CASES_DIR / f"{name}.py"
    assert path.exists()

    return LoadedCase(name=name, path=path)


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("case", callback=handle_case)
@click.option(
    "--https", is_flag=True, default=False, help="Make requests against an HTTPS server"
)
def run(case: LoadedCase, https: bool) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    TMP_DIR.mkdir(exist_ok=True)

    out = str(OUTPUT_DIR / case.out)
    target = str(case.path)

    config = Config(host="localhost", port=8123, num_requests=1000, https=https)
    main = load_case_entrypoint(target)

    with config.server():
        if inspect.iscoroutinefunction(main):

            async def coro() -> None:
                with record_profile(out):
                    await main(config)

            asyncio.run(coro())
        else:
            with record_profile(out):
                main(config)


@cli.command()
@click.argument("case", callback=handle_case)
def view(case: LoadedCase) -> None:
    args = ["snakeviz", str(OUTPUT_DIR / case.out)]
    subprocess.run(args)


if __name__ == "__main__":
    import sys

    sys.exit(cli())
