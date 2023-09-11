#import textwra
import urllib.parse
from datetime import datetime
from pprint import pformat  # リストや辞書を整形して出力する'pprint'を使用する
# from typing import Tuple, Optional
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
from common.template.renderer import render
import csv
# For multipart
import cgi
#import base64
import io
from cgi import FieldStorage

# import requests

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

def upload(request: HTTPRequest) -> HTTPResponse: # type: ignore
    # GETリクエストの場合は、405を返す
    if request.method == "GET":
        body = b"<html><body><h1>405 Method Not Allowed</h1></body></html>"
        return HTTPResponse(body=body, status_code=405)

    # POTリクエストの場合は、アップロードしたfileを開く
    elif request.method == "POST":
        """_summary_
        5つの変数(method: str, path: str, http_version: str, request_header: dict, request_body: bytes)を
        HTTPRequestでオブジェクト化
        これらは見当たらない？
        # print("views: HTTPRequest = ", request.status_code)
    
        ※ちなみに、multipart/form-data形式で送られてきた内容をパースするには、
        pythonではcgiモジュールのFieldStorageというクラスを利用します。
        """
        file, file_name = parse_multipart_form(request)
        
        print("view190_file", file)
        
        rows = []
        csv_reader = csv.reader(file.splitlines(), delimiter=',')
        print("view193_csv_reader = ", csv_reader)
        for row in csv_reader:
            print("view194_row = ", row)
            rows.append(row)
            
        # file = open(file_name, "rb")        
        # data_list = file.readlines()
        # print("view193_data_list", data_list)
        
        # for data in data_list:
        #     print("view196_data", data, end ="")
        # print()
            
        # print("views190_data_list",data_list)
        # for data in data_list:
        #     print("views193_data", data, end = "")
        # print()
        # File.close()
        # header = request.headers
        # print("views_186: headers = ", header)
        # print("views_187: content_type = ", header['Content-Type'])
        # print("views_188: cookie = ", header['Cookie'])
        # body = request.body.decode() 
        # print("views_190: request.body = ", body)
        # files = request.files.decode()
        # print("views_191: file = ", type(files))
        # bodyはstr
        # print("views_193: body = ", body.items(),type(body))
        
        # post_params = urllib.parse.parse_qs(request.body.decode())
        # print("post_params", post_params)
        # response_body = textwrap.dedent(html).encode()
        # body = textwrap.dedent(html).encode()
        # # Content-Typeを指定
        # content_type = "text/html; charset=UTF-8"
        
        # # header = urllib.parse.parse_qs(request.header.decode())
        # contents = urllib.parse.parse_qs(request.body.decode())
        
        # # with open("post_request_body.text", "wb") as f:
        # #     f.write(body) # type: ignore
    
        # file = request.FILE
    
        # print("file = ", file)
        # if not file:
        #     return 'ファイルアップロードされていません.', 400
        # if file.filename.endswith('.csv'):
        #     rows = []
        #     csv_file = file.stream.read().decode("SHIFT-JIS")
        #     csv_reader = csv.reader(csv_file.splitlines(), delimiter=',')
        #     for row in csv_reader:
        #         rows.append(row)
        #     return render_template('table.html', rows=rows)
        # else:
        #     return 'CSVファイルではありません.', 400
        # # print("request",params[])
        # # print("file_name",file_name)
        
        context = {
            "request": request, 
            "headers": pformat(request.headers), 
            "body": request.body.decode("utf-8", "ignore"),
            "filename": file_name,
            "file": file,
            "rows": rows,
        }
        body = render("upload.html", context)
        
        return HTTPResponse(body=body) # type: ignore
    
def parse_multipart_form(request: HTTPRequest):
    # cgi.FieldStorageのバッファーポインターを設定
    fp = io.BytesIO(request.body)
    # print("view242_fp = ", fp, type(fp))
    environ = {'REQUEST_METHOD': 'POST'}
    headers = {
        'content-type': request.headers['Content-Type'],
        'content-length': request.headers['Content-Length'],
    }
    form = cgi.FieldStorage(fp = fp, environ = environ, headers = headers)
    print("views259_form = ", form, type(form))
    print("views260_form.list = ", form.list, type(form.list), len(form.list))
    
    list = form.getlist("name")
    print("view263_list = ", list)
    
    for f  in form.list:
        if f.name == "file_name":
            print("views264_f.name = ", f.name)             # file_name
            print("views265_f.filename = ", f.filename)     # testNew_14.csv
            print("views266_f.type = ", f.type)             # text/csv = 
            print("views267_f.value = ", f.value)           #
        # print("views263_form.list = ", f.name, f.filename, f.type, f.value)
        # print("views264_f.name = ", f.name)
        # print("views265_f.filename = ", f.filename)
        # print("views266_f.type = ", f.type)
        # print("views267_f.value = ", f.value)
    # file: str
    # file_name: str
    files = form['file_name']
    file = files.value.decode()
    file_name =files.filename
    print('view280_file = ',files)
    print('view281_file_name = ',file_name)
    # if form.value != None:
    
    #     print("view265_form.value = ", form.value)
    #     for f in form.value:
    #         if f.filename:
    #             file = f.value.decode()
    #             file_name = f.filename
    
    return file, file_name