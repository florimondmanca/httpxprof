import httpx
import tqdm

from httpxprof.config import NUM_REQUESTS, SERVER_URL


with httpx.Client() as client:
    for _ in tqdm.tqdm(range(NUM_REQUESTS)):
        client.get(SERVER_URL)
