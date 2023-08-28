import textwrap
import urllib.parse
from datetime import datetime
from pprint import pformat  # リストや辞書を整形して出力する'pprint'を使用する
# from typing import Tuple, Optional
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
from common.template.renderer import render

"""
現在時刻を表示するHTMLを生成する
"""
def now(request: HTTPRequest) -> HTTPResponse:
    """_summary_
    5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
    HTTPRequestでオブジェクト化
    Args:
        request (HTTPRequest): _description_
    Returns:
        HTTPResponse: _description_
    """
    context = {"now": datetime.now()}
    
    # html = render("./templates/now.html", context)
    # html = render("now.html", context)
    """
    HTMLファイルのオープンをcommon.template.rendererに集約
    with open("./templates/now.html") as f:
        template = f.read()
        html = template.format(now=datetime.now())
    
    また、htmlをtemplates下にまとめる"
    response_body = textwrap.dedent(html).encode()
    body = textwrap.dedent(html).encode()
    """
    # body = html.encode()
    body = render("now.html", context)
    # Content-Typeを指定
    # content_type = "text/html; charset=UTF-8"
    # レスポンスラインを生成
    # response_line = "HTTP/1.1 200 OK\r\n"
    
    # return response_body, content_type, response_line
    # return HTTPResponse(body=body, content_type=content_type, status_code=200)
    return HTTPResponse(body=body) # type: ignore

def show_request(request: HTTPRequest) -> HTTPResponse:
    """_summary_
    5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
    HTTPRequestでオブジェクト化
    Args:
        request (HTTPRequest): _description_

    Returns:
        HTTPResponse: _description_
    """
    """
    HTTPリクエストの内容を表示するHTMLを生成する
    """
    # html = f"""\
    #     <html>
    #     <body>
    #         <h1>Request Line:</h1>
    #         <p>
    #             {request.method} {request.path} {request.http_version}
    #         </p>
    #         <h1>Headers:</h1>
    #         <pre>{pformat(request.headers)}</pre>
    #         <h1>Body:</h1>
    #         <pre>{request.body.decode("utf-8", "ignore")}</pre>
    #     </body>
    #     </html>
    # """
    # response_body = textwrap.dedent(html).encode()
    context = {"request": request, "headers": pformat(request.headers), "body": request.body.decode("utf-8", "ignore")}
    body = render("show_request.html", context)
    
    #body = textwrap.dedent(html).encode()
    # Content-Typeを指定
    #content_type = "text/html; charset=UTF-8"
    # レスポンスラインを生成
    # response_line = "HTTP/1.1 200 OK\r\n"
    
    # return response_body, content_type, response_line
    # return HTTPResponse(body=body, content_type=content_type, status_code=200)
    return HTTPResponse(body=body) # type: ignore


def parameters(request: HTTPRequest) -> HTTPResponse:
    """_summary_
    5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
    HTTPRequestでオブジェクト化
    Args:
        request (HTTPRequest): _description_

    Returns:
        HTTPResponse: _description_
    """
    """
    POSTパラメータを表示するHTMLを表示する
    """
    # GETリクエストの場合は、405を返す
    # if method == "GET":
    if request.method == "GET":
        # response_body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        #content_type = "text/html; charset=UTF-8"
        # response_line = "HTTP/1.1 405 Method Not Allowed\r\n"
        #status_code = 405
        return HTTPResponse(body=body, status_code=405)

    # elif method == "POST":
    elif request.method == "POST":
        # post_params = urllib.parse.parse_qs(request_body.decode())
        # post_params = urllib.parse.parse_qs(request.body.decode())
        # # html = f"""\
        # #     <html>
        # #     <body>
        # #         <h1>Parameters:</h1>
        # #         <pre>{pformat(post_params)}</pre>                        
        # #     </body>
        # #     </html>
        # # """
        # # response_body = textwrap.dedent(html).encode()
        # body = textwrap.dedent(html).encode()
        # # Content-Typeを指定
        # content_type = "text/html; charset=UTF-8"
        # # レスポンスラインを生成
        # # response_line = "HTTP/1.1 200 OK\r\n"
        # status_code = 200
        
        context = {"params": urllib.parse.parse_qs(request.body.decode())}
        body = render("parameters.html", context)

        return HTTPResponse(body=body)
        
    # return response_body, content_type, response_line
    return HTTPResponse(body=body, content_type=content_type, status_code=status_code)  # type: ignore

def user_profile(request: HTTPRequest) -> HTTPResponse:
    # user_id = request.params["user_id"]
    # # html = f"""\
    # #     <html>
    # #     <body>
    # #         <h1>プロフィール</h1>
    # #         <p>ID: {user_id}
    # #     </body>
    # #     </html>
    # # """
    # body = textwrap.dedent(html).encode()
    # content_type = "text/html; charset=UTF-8"
    # status_code = 200
    
    context = {"user_id": request.params["user_id"]}
    body = render("user_profile.html", context)

    return HTTPResponse(body=body)