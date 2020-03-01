import asyncio

import httpx

import httpxprof


async def main() -> None:
    async with httpx.AsyncClient() as client:
        for _ in httpxprof.requests():
            await client.get(httpxprof.url)


asyncio.run(main())
