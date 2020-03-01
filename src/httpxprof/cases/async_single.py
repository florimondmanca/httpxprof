import asyncio

import httpx

import httpxprof


async def main() -> None:
    for _ in httpxprof.requests():
        async with httpx.AsyncClient() as client:
            await client.get(httpxprof.url)


asyncio.run(main())
