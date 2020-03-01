import asyncio

import httpx
import tqdm

from httpxprof.config import NUM_REQUESTS, SERVER_URL


async def main() -> None:
    async with httpx.AsyncClient() as client:
        for _ in tqdm.tqdm(range(NUM_REQUESTS)):
            await client.get(SERVER_URL)


asyncio.run(main())
