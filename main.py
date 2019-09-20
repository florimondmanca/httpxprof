import os
import pathlib
import subprocess
import time

import click
import uvicorn
import snakeviz

OUTPUT_DIR = pathlib.Path("out")
BENCHES_DIR = pathlib.Path("benches")
BENCHES = [filename.rstrip(".py") for filename in os.listdir(BENCHES_DIR)]


@click.group()
def cli():
    pass


@cli.command()
def serve():
    uvicorn.run("server:app")


@cli.command()
@click.argument("bench", type=click.Choice(BENCHES))
def run(bench: str) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    out = str(OUTPUT_DIR / f"{bench}.prof")
    script = str(BENCHES_DIR / f"{bench}.py")

    args = ["python", "-m", "cProfile", "-o", out, script]
    start = time.perf_counter()
    subprocess.run(args)
    elapsed = time.perf_counter() - start
    click.echo(f"Took {elapsed:.2f} seconds")


@cli.command()
@click.argument("bench", type=click.Choice(BENCHES))
def view(bench: str) -> None:
    args = ["snakeviz", str(OUTPUT_DIR / f"{bench}.prof")]
    subprocess.run(args)


if __name__ == "__main__":
    cli()
