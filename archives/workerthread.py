import os
import re
# import textwrap
import traceback
# import urllib.parse # for POST method 
from datetime import datetime
#from pprint import pformat  # リストや辞書を整形して出力する'pprint'を使用する
from socket import socket
from threading import Thread
# from typing import Tuple, Optional
from typing import Tuple

import views
from common.http.request import HTTPRequest
from common.http.response import HTTPResponse
#from urls import URL_VIEW # type: ignore
from common.urls.resolver import URLResolver

class WorkerThread(Thread):
    # 実行ファイルのあるディレクトリ
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 静的配信するファイルを置くディレクトリ
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    
    # 拡張子とMIME Typeの対応
    MIME_TYPES = {
        "html": "text/html; charset=UTF-8",
        "css": "text/css",
        "png": "image/png",
        "jpg": "image/jpg",
        "gif": "image/gif",
    }
    
    # # pathとview関数の対応
    # URL_VIEW = {
    #     "/now": views.now,
    #     "/show_request": views.show_request,
    #     "/parameters": views.parameters,
    # }
    
        # ステータスコードとステータスラインの対応
    STATUS_LINES = {
        200: "200 OK",
        404: "404 Not Found",
        405: "405 Method Not Allowed",
    }
    
    def __init__(self, client_socket: socket, address: Tuple[str, int]):
        super().__init__()
        
        self.client_socket = client_socket
        self.client_address = address
        
    def run(self) -> None:
        """
        クライアントと接続済みのsocketを引数として受け取り、
        リクエストを処理してレスポンスを送信する
        """
        try:
            # クライアントから送られてきたデータを取得する
            request_bytes = self.client_socket.recv(4096)

            # クライアントから送られてきたデータをファイルに書き出す
            with open("server_recv.txt", "wb") as f:
                f.write(request_bytes)

            # HTTPリクエストをパースする
            # method, path, http_version, request_header, request_body = self.parse_http_request(request)
            request = self.parse_http_request(request_bytes)
            
            # # 代入箇所が複数に分かれてしまっているので、事前に型注釈を置く
            # response_body: bytes
            # content_type: Optional[str] # strまたはNoneを表す型
            # response_line: str
            
            # pathに対応するview関数があれば、関数を取得して呼び出し、レスポンスを生成する
            # if path in self.URL_VIEW:
            # if request.path in self.URL_VIEW:
            if request.path in URL_VIEW:
                # view = self.URL_VIEW[path]
                # view = self.URL_VIEW[request.path]
                view = URL_VIEW[request.path]
                # response_body, content_type, response_line = view(
                #     method, path, http_version, request_header, request_body
                # )
                response = view(request)
                    
            # pathがそれ以外のときは、静的ファイルからレスポンスを生成する
            else:
                try:
                    # ファイルからレスポンスボディを生成
                    # response_body = self.get_static_file_content(path)
                    response_body = self.get_static_file_content(request.path)
                    # Content-Typeを指定
                    content_type = None
                    # レスポンスラインを生成
                    # response_line = "HTTP/1.1 200 OK\r\n"
                    response = HTTPResponse(body=response_body, content_type=content_type, status_code=200) # type: ignore
                                
                except OSError:
                    # レスポンスを取得できなかった場合は、ログを出力して404を返す
                    traceback.print_exc()
                    
                    response_body = b"<html><body><h1>404 Not Found</h1></body></html>"
                    content_type = "text/html; charset=UTF-8"
                    # response_line = "HTTP/1.1 404 Not Found\r\n"
                    response = HTTPResponse(body=response_body, content_type=content_type, status_code=404)

            # レスポンスラインを生成
            response_line = self.build_response_line(response)
            # レスポンスヘッダーを生成
            # response_header = self.build_response_header(path, response_body, content_type)
            response_header = self.build_response_header(response, request)
            # レスポンス全体を生成する
            # response = (response_line + response_header + "\r\n").encode() + response_body
            response_bytes = (response_line + response_header + "\r\n").encode() + response.body # type: ignore

            # クライアントへレスポンスを送信する
            # self.client_socket.send(response)
            self.client_socket.send(response_bytes)
                
        except Exception:
            # リクエストの処理中に例外が発生した場合はコンソールにエラーログを出力し、
            # 処理を続行する
            print("=== Worker: リクエストの処理中にエラーが発生しました ===")
            traceback.print_exc()
            
        finally:
            # 例外が発生した場合も、発生しなかった場合も、TCP通信のcloseは行う
            print(f"=== Worker: クライアントとの通信を終了します remote_address: {self.client_address} ===")
            self.client_socket.close()

    # def parse_http_request(self, request: bytes) -> Tuple[str, str, str, dict, bytes]:
    def parse_http_request(self, request: bytes) -> HTTPRequest:
        """
        生のHTTPリクエストを
        1. method: str
        2. path: str
        3. http_version: str
        4. request_header: dict
        5. request_body: bytes
        に分割/変換する
        """
        # リクエスト全体を
        # - リクエストライン(1行目)
        # - リクエストヘッダー(2行目〜空行)
        # - リクエストボディ(空行〜)
        # にパースする
        request_line, remain = request.split(b"\r\n", maxsplit=1)
        request_header, request_body = remain.split(b"\r\n\r\n", maxsplit=1)

        # リクエストラインを文字列に変換してパースする
        method, path, http_version = request_line.decode().split(" ")
        
        # リクエストヘッダーを辞書にパースする
        headers = {}
        for header_row in request_header.decode().split("\r\n"):
            key, value = re.split(r": *", header_row, maxsplit=1)
            headers[key] = value        

        # return method, path, http_version, headers, request_body
        return HTTPRequest(method=method, path=path, http_version=http_version, headers=headers, body=request_body)   

    def get_static_file_content(self, path: str) -> bytes:
        """
        リクエストpathから、staticファイルの内容を取得する
        """
        # pathの先頭の/を削除し、相対パスにしておく
        relative_path = path.lstrip("/")
        # ファイルのpathを取得
        static_file_path = os.path.join(self.STATIC_ROOT, relative_path)

        with open(static_file_path, "rb") as f:
            return f.read()

    def build_response_line(self, response: HTTPResponse) -> str:
        """
        レスポンスラインを構築する
        """
        status_line = self.STATUS_LINES[response.status_code]
                
        return f"HTTP/1.1 {status_line}\r\n"
        
    def build_response_header(self, response: HTTPResponse, request: HTTPRequest) -> str:
    # def build_response_header(self, path: str, response_body: bytes, content_type: Optional[str]) -> str:
        """
        レスポンスヘッダーを構築する
        """
        # Content-Typeが指定されていない場合はpathから特定する
        # if content_type is None:
        if response.content_type is None:
            # pathから拡張子を取得
            # if "." in path:
            if "." in request.path:
                # ext = path.rsplit(".", maxsplit=1)[-1]
                ext = request.path.rsplit(".", maxsplit=1)[-1]
            else:
                ext = ""
            # 拡張子からMIME Typeを取得
            # 知らない対応していない拡張子の場合はoctet-streamとする
            # content_type = self.MIME_TYPES.get(ext, "application/octet-stream")
            response.content_type = self.MIME_TYPES.get(ext, "application/octet-stream")

        response_header = ""
        response_header += f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}\r\n"
        response_header += "Host: Test_Server/0.1\r\n"
        # response_header += f"Content-Length: {len(response_body)}\r\n"
        response_header += f"Content-Length: {len(response.body)}\r\n"
        response_header += "Connection: Close\r\n"
        # response_header += f"Content-Type: {content_type}\r\n"
        response_header += f"Content-Type: {response.content_type}\r\n"

        return response_header
        