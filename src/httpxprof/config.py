import pathlib
import typing

import tqdm

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8123
SERVER_URL = f"http://{SERVER_HOST}:{SERVER_PORT}"

NUM_REQUESTS = 1000

OUTPUT_DIR = pathlib.Path(__file__).parent / "out"
CASES_DIR = pathlib.Path(__file__).parent / "cases"
assert CASES_DIR.exists(), CASES_DIR


def requests() -> typing.Iterator[None]:
    for _ in tqdm.tqdm(range(NUM_REQUESTS)):
        yield
