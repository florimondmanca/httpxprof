import httpx
import tqdm

from httpxprof.config import NUM_REQUESTS, SERVER_URL


for _ in tqdm.tqdm(range(NUM_REQUESTS)):
    with httpx.Client() as client:
        client.get(SERVER_URL)
