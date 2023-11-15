from enum import Enum

class HTTPMethod(str, Enum):
    CONNECT: str
    DELETE: str
    GET: str
    HEAD: str
    OPTIONS: str
    PATCH: str
    POST: str
    PUT: str
    TRACE: str
