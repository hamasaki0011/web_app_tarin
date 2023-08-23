import socket
import sys
import traceback
from typing import Tuple

HOST = "127.0.0.1"
PORT = 8080
METHOD = "GET"
PATH = "/index.html"
HTML_VERSION = "HTTP/1.1"

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
            request_header = self.build_request_handler(METHOD, PATH, HTML_VERSION)
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
            
            # #　レスポンス全体を解析する
            status_code, code_remark, date, host = self.parse_http_response(response)
            
            if status_code == "200" and code_remark == "OK":
                print(f"=== <{METHOD}>メソッドで",end='')
                print(f"≪ {host} ≫ に接続しました ===")
                print(f"=== {date} ===")                  
            #　レスポンスの内容をコンソールに表示する
            else:
                print("=== 指定されたサイトへの接続は失敗しました ===")
                    
            # 通信を終了させる
            client_socket.close() # type: ignore            
        
        except  ConnectionRefusedError:
            # ポート番号指定違いで接続拒否
            print(f"=== 'http://{HOST}:{PORT}{PATH}'に接続拒否されました！ ===")
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
        client_socket.connect((HOST, PORT)) # 127.0.0.1
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
            request_header = ""
            request_header += "Host: TestServer/0.1\r\n"
            request_header += "Connection: keep-alive\r\n"
            request_header += "Cache-Control: max-age=0\r\n"
            request_header += "sec-ch-ua: 'Chromium';v='116', 'Not)A;Brand';v='24', 'Google Chrome';v='116'\r\n"
            request_header += "sec-ch-ua-mobile: ?0\r\n"
            request_header += "sec-ch-ua-platform: 'Windows'\r\n"
            request_header += "Upgrade-Insecure-Requests: 1\r\n"
            request_header += "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36\r\n"
            request_header += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7\r\n"
            request_header += "Sec-Fetch-Site: none\r\n"
            request_header += "Sec-Fetch-Mode: navigate\r\n"
            request_header += "Sec-Fetch-User: ?1\r\n"
            request_header += "Sec-Fetch-Dest: document\r\n"
            request_header += "Accept-Encoding: gzip, deflate, br\r\n"
            request_header += "Accept-Language: ja,en-US;q=0.9,en;q=0.8\r\n"
            
            return request_line + request_header
        
    def parse_http_response(self, response:bytes) -> Tuple[str, str, str, str]:
            #　レスポンス全体を解析する
            #　①行目　レスポンスライン
            #　②行目～レスポンスヘッダー
            #　③行目～空行～ボディ
            response_line, remain = response.split(b"\r\n",maxsplit=1)
            response_header, response_body = remain.split(b"\r\n\r\n", maxsplit=1)
            
            # レスポンスラインを解析
            http_version, status_code, code_remark = response_line.decode().split(" ")

            date, host, content_length, connection, content_type = response_header.decode().split("\r\n")
            temp,host = host.split(" ")
            
            # print("日付けは ",date)
            # print("ホストは ",host)
            # print("長さは ",content_length)
            # print("接続は ",connection)
            # print("タイプは ",content_type)
            
            return status_code, code_remark, date, host 


if __name__ == '__main__':
    client = TCPClient()
    client.request()
