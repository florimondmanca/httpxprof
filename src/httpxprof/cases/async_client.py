import httpx

import httpxprof


async def main(config: httpxprof.Config) -> None:
    async with httpx.AsyncClient(verify=config.client_cert() or False) as client:
        for _ in config.requests():
            await client.get(config.url)
