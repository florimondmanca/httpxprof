import httpx

import httpxprof


with httpx.Client() as client:
    for _ in httpxprof.requests():
        client.get(httpxprof.url)
