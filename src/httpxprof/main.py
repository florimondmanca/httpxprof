import os
import subprocess

import click

from .config import CASES_DIR, OUTPUT_DIR, SERVER_HOST, SERVER_PORT
from .utils import server

CASES = [
    filename.rstrip(".py")
    for filename in os.listdir(CASES_DIR)
    if filename != "__init__.py"
]


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("case", type=click.Choice(CASES))
def run(case: str) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    out = str(OUTPUT_DIR / f"{case}.prof")
    target = str(CASES_DIR / f"{case}.py")

    args = ["python", "-m", "cProfile", "-o", out, target]

    with server(host=SERVER_HOST, port=SERVER_PORT):
        subprocess.run(args)


@cli.command()
@click.argument("case", type=click.Choice(CASES))
def view(case: str) -> None:
    args = ["snakeviz", str(OUTPUT_DIR / f"{case}.prof")]
    subprocess.run(args)


if __name__ == "__main__":
    import sys

    sys.exit(cli())
