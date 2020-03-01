import httpx

import httpxprof

for _ in httpxprof.requests():
    with httpx.Client() as client:
        client.get(httpxprof.url)
