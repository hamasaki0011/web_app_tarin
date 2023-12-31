import os
import traceback
import settings
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse

"""
静的ファイルからレスポンスを取得する
見つからなかったときは、404 Not Found を返す
"""
def static(request: HTTPRequest) -> HTTPResponse:

    try:
        static_root = getattr(settings, "STATIC_ROOT")

        # pathの先頭の/を削除し、相対パスにしておく
        relative_path = request.path.lstrip("/")
        # ファイルのpathを取得
        static_file_path = os.path.join(static_root, relative_path)

        with open(static_file_path, "rb") as f:
            response_body = f.read()

        content_type = None
        
        return HTTPResponse(body=response_body, content_type=content_type, status_code=200) # type: ignore

    except OSError:
        # ファイルを取得できなかった場合は、ログを出力して404を返す
        traceback.print_exc()

        response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
        content_type = "text/html;"
        return HTTPResponse(body=response_body, content_type=content_type, status_code=404)