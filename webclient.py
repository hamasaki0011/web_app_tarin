import socket   # Socket
import re       # 正規表現
import sys
import traceback
from typing import Tuple

# HOST = "httpbin.org"    #"10.10.210.87"   #"127.0.0.1"
# PORT = 80
# METHOD = "POST"  #"GET"
# PATH = "/post"   #"/record/record/article/"   #"/form.html"  #"/show_request"   #"/now"   #"/index.html"
# HTML_VERSION = "HTTP/1.1"

# Request headers
req_header = {
    # "HOST": "httpbin.org",    # Request method test site
    # "PORT": 80,               # default port number
    # "METHOD": "POST",         # "GET"
    # "PATH": "/post",          # "/get"
    
    # "HOST": "127.0.0.1",        # "10.10.210.87"
    # "PORT": 8080,               # 8000
    # "METHOD": "GET",            # "POST"
    # "PATH": "/now",      # "/form.html" "/show_request" "/now" "/index.html" 

    "HOST": "127.0.0.1",        # "10.10.210.87"
    "PORT": 8080,               # 8000
    "METHOD": "POST",            # "POST"
    "PATH": "/index.html",      # "/form.html" "/show_request" "/now" "/index.html" 
    
    "VERSION": "HTTP/1.1",      # HTTP version
    
    }

class TCPClient:
    """
    TCP通信を行うクライアントを表すクラス
    """
    def request(self):
        """
        サーバーへリクエストを送信する
        """
        print("=== クライアントを起動します ===")
        
        try:
            # client_socketを生成
            client_socket = self.create_client_socket()
            # リクエスト(request_line + request_header)を生成してサーバーに送る
            request_header = self.build_request_handler(req_header['METHOD'], req_header['PATH'], req_header['VERSION'])
            # ヘッダーをbytesに変換し、リクエストを生成する
            #request = (request_line + request_header + "\r\n").encode() + request_body
            request = (request_header + "\r\n").encode()    
            # サーバーへリクエストを送信する
            client_socket.send(request) # type: ignore
            # サーバーからレスポンスが送られてくるのを待って取得する
            response = client_socket.recv(4096) # type: ignore
            # レスポンスの内容を、ファイルに書き出す
            with open("web_client_recv.txt", "wb") as f:
                f.write(response)
            
            # @2023.8.23 for debugging print("response= ",response)
            # #　レスポンス全体を解析する
            html_version, code_status, code_remark, header = self.parse_http_response(response)
          
            #　レスポンスの内容をコンソールに表示する
            if code_status == "200" and code_remark == "OK":
                print(f"=== <{req_header['METHOD']}>メソッドで",end='')
                print(f"≪ {req_header['HOST']} ≫ に接続しました@", end='')
                print(f"{header['Date']} ===")                  
            
            elif code_status == "404":
                print("=== Not Found: 指定されたサイトが見つかりません ===")
                
            elif code_status == "405":
                print("=== Method Not Allowed: 指定されたサイトにアクセスできません ===")
    
            else:
                print("=== 指定されたサイトへの接続は失敗しました ===")
                    
            # 通信を終了させる
            client_socket.close() # type: ignore            
        
        except  ConnectionRefusedError:
            # ポート番号指定違いで接続拒否
            print(f"=== 'http://{req_header['HOST']}:{req_header['PORT']}{req_header['PATH']}'に接続拒否されました！ ===")
            # 2023.8.23　後でlogファイル作成に書き換える
            #traceback.print_exc()
            
        finally:
            print("=== クライアントからのアクセスを停止します。 ===")

    def create_client_socket(self) -> socket: # type: ignore
        """
        サーバーと通信するためclient_socketを生成する
        :return:
        """       
        # socketの生成
        client_socket = socket.socket()
        client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # サーバーと接続する 8080
        #print("=== サーバーと接続します ===")
        client_socket.connect((req_header['HOST'], req_header['PORT']))
        print("=== サーバーと接続しました ======")
        return client_socket # type: ignore
                    
    def build_request_handler(self, method: str, path: str, html_version: str):
            # 2023.8.23 request_bodyを生成するケースを考慮してコメントとして残す
            # ファイルからrequest_bodyを生成する
            #with open("web_client_send.txt", "rb") as f:
            #    request_body = f.read()
                    
            # request_lineを生成
            request_line = method + " " + path + " " + html_version + "\r\n"
            
            # requestヘッダーを生成
            # 「Cache-Control: max-age=0」を加えると、レスポンスが遅くなる。
            request_header = ""
            # request_header += "Host: TestServer/0.1\r\n"
            request_header += "Host: " + req_header['HOST'] + "\r\n"
            request_header += "Connection: keep-alive\r\n"
            # request_header += "Cache-Control: max-age=100\r\n"
            request_header += "sec-ch-ua: 'Chromium';v='116', 'Not)A;Brand';v='24', 'Google Chrome';v='116'\r\n"
            request_header += "sec-ch-ua-mobile: ?0\r\n"
            request_header += "sec-ch-ua-platform: 'Windows'\r\n"
            request_header += "Upgrade-Insecure-Requests: 1\r\n"
            request_header += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\r\n"
            request_header += "Accept: text/html,application/xhtm”l+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
            request_header += "Sec-Fetch-Site: none\r\n"
            request_header += "Sec-Fetch-Mode: navigate\r\n"
            request_header += "Sec-Fetch-User: ?1\r\n"
            request_header += "Sec-Fetch-Dest: document\r\n"
            request_header += "Accept-Encoding: gzip, deflate, br\r\n"
            request_header += "Accept-Language: ja,en-US;q=0.9,en;q=0.8\r\n"
            
            return request_line + request_header
        
    def parse_http_response(self, response:bytes) -> Tuple[str, str, str, dict]:
            #　レスポンス全体を解析する
            #　①行目　レスポンスライン
            #　②行目～レスポンスヘッダー
            #　③行目～空行～ボディ
            response_line, remain = response.split(b"\r\n",maxsplit=1)
            # レスポンスラインをHTMLバージョン、コード、コメントの3つに分割する
            version, code, remark = response_line.decode().split(" ",maxsplit=2)
            # for debugging@2023.8.24 print("remark= ", remark)
            
            # レスポンスヘッダーを抜き出す
            response_header, response_body = remain.split(b"\r\n\r\n", maxsplit=1)
            # レスポンスヘッダーを辞書にパースする
            headers = {}
            for header_row in response_header.decode().split("\r\n"):
                # response_headerをデコードして、一行毎読み込む
                # 各行に対して１つの':'と0個以上の空白を表す正規表現で分割して、keyとvalueを取得して
                key, value = re.split(r": *", header_row, maxsplit=1)
                # 取得したkeyとvalueで辞書型に変換
                headers[key] = value 
            
            # print(headers)
            # print(f"ヘッダーの項目数は、{len(headers)}個")
            # print("日付けは ",Date)
            # print("ホストは ",Host)
            # print("長さは ",Content-length)
            # print("接続は ",Connection)
            # print("タイプは ",Content-type)
            
            return version, code, remark, headers 

if __name__ == '__main__':
    client = TCPClient()
    client.request()
