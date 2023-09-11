"""_summary_ HTTP Requestを表現するクラス
いくつかのデータをまとめて、一つのパラメータとして扱う
デコレータ：@dataclassを使用した例
from dataclasses import dataclass, field

@dataclass
class HTTPRequest:
    path: str
    method: str
    http_version: str
    headers: dict = field(default_factory=dict)
    body: bytes
    
クラスの使用例：
request = HTTPRequest(
    method="POST",
    path="/index.html",
    http_version="HTTP/1.1",
    headers={
        "HOST": "localhost:8080",
    },
    body=b"foo=bar&foo2=bar2"
)
print(request.method)  # "POST"
print(request.path)  # "/index.html" 

"""
class HTTPRequest:
    path: str
    method: str
    http_version: str
    headers: dict
    body: bytes
    params: dict

    def __init__(
        self, path: str = "",
        method: str = "",
        http_version: str = "",
        headers: dict = None, # type: ignore
        body: bytes = b"",
        params: dict = None, # type: ignore
    ):
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        self.path = path
        self.method = method
        self.http_version = http_version
        self.headers = headers
        self.body = body
        self.params = params
