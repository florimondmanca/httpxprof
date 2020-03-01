import httpx

import httpxprof


def main(config: httpxprof.Config) -> None:
    for _ in config.requests():
        with httpx.Client(verify=config.client_cert() or False) as client:
            client.get(config.url)
