import httpx

import httpxprof


async def main(config: httpxprof.Config) -> None:
    for _ in config.requests():
        async with httpx.AsyncClient(verify=config.client_cert() or False) as client:
            await client.get(config.url)
