import asyncio

import httpx
import tqdm

from httpxprof.config import NUM_REQUESTS, SERVER_URL


async def main() -> None:
    for _ in tqdm.tqdm(range(NUM_REQUESTS)):
        async with httpx.AsyncClient() as client:
            await client.get(SERVER_URL)


asyncio.run(main())
