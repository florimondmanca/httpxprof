async def app(scope, receive, send):
    assert scope["type"] == "http"
    res = b"Hello, world"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
                [b"content-length", b"%d" % len(res)],
            ],
        }
    )
    await send({"type": "http.response.body", "body": res})
