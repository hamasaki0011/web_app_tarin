#import textwrap
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

"""
HTTPリクエストの内容を表示するHTMLを生成する
"""
def show_request(request: HTTPRequest) -> HTTPResponse:
    """_summary_
    5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
    HTTPRequestでオブジェクト化
    """
    """
    HTML移動
    """
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

"""
POSTパラメータを表示するHTMLを表示する
"""
def parameters(request: HTTPRequest) -> HTTPResponse:
    """_summary_
    5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
    HTTPRequestでオブジェクト化
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
        # post_params = urllib.parse.parse_qs(request.body.decode())
        # # response_body = textwrap.dedent(html).encode()
        # body = textwrap.dedent(html).encode()
        # # Content-Typeを指定
        # content_type = "text/html; charset=UTF-8"
        # # レスポンスラインを生成
        # # response_line = "HTTP/1.1 200 OK\r\n"
        # status_code = 200
        
        context = {"params": urllib.parse.parse_qs(request.body.decode())}
        body = render("parameters.html", context)

        return HTTPResponse(body=body) # type: ignore
        
    # return response_body, content_type, response_line
    return HTTPResponse(body=body, content_type=content_type, status_code=status_code)  # type: ignore

def user_profile(request: HTTPRequest) -> HTTPResponse:
    # user_id = request.params["user_id"]
    # body = textwrap.dedent(html).encode()
    # content_type = "text/html; charset=UTF-8"
    # status_code = 200
    
    context = {"user_id": request.params["user_id"]}
    body = render("user_profile.html", context)

    return HTTPResponse(body=body) # type: ignore

# 2023.8.28 In order to check cookies'
def set_cookie(request: HTTPRequest) -> HTTPResponse:
    return HTTPResponse(headers={"Set-Cookie": "username=fujico"})

# 2023.8.29 In order to check login function
def login(request: HTTPRequest) -> HTTPResponse: # type: ignore
    # GETリクエストのとき、単にテンプレートHTMLを表示
    if request.method == "GET":
        body = render("login.html", {})
        return HTTPResponse(body=body) # type: ignore

    # POSTリクエストのときは、リクエストボディからPOSTパラメータを抽出しusernameを取得する。
    elif request.method == "POST":
        post_params = urllib.parse.parse_qs(request.body.decode())
        username = post_params["username"][0]

        # ヘッダーが生成されるようにしてレスポンスを返却
        headers = {"Location": "/welcome", "Set-Cookie": f"username={username}"}
        return HTTPResponse(status_code=302, headers=headers)
    
def welcome(request: HTTPRequest) -> HTTPResponse:
    cookie_header = request.headers.get("Cookie", None)

    # Cookieが送信されてきていなければ、ログインしていないとみなして/loginへリダイレクト
    if not cookie_header:
        return HTTPResponse(status_code=302, headers={"Location": "/login"})

    # str から list へ変換
    # ex) "name1=value1; name2=value2" => ["name1=value1", "name2=value2"]
    cookie_strings = cookie_header.split("; ")

    # list から dict へ変換
    # ex) ["name1=value1", "name2=value2"] => {"name1": "value1", "name2": "value2"}
    cookies = {}
    for cookie_string in cookie_strings:
        name, value = cookie_string.split("=", maxsplit=1)
        cookies[name] = value

    # Cookieにusernameが含まれていなければ、ログインしていないとみなして/loginへリダイレクト
    if "username" not in cookies:
        return HTTPResponse(status_code=302, headers={"Location": "/login"})

    # Welcome画面を表示
    body = render("welcome.html", context={"username": cookies["username"]})

    return HTTPResponse(body=body) # type: ignore
