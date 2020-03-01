import pathlib
import typing


Pathlike = typing.Union[str, pathlib.Path]


class Certificates(typing.NamedTuple):
    server_key: pathlib.Path
    server_cert: pathlib.Path
    client_cert: pathlib.Path
