import httpx

import httpxprof


def main(config: httpxprof.Config) -> None:
    with httpx.Client(verify=config.client_cert() or False) as client:
        for _ in config.requests():
            client.get(config.url)
