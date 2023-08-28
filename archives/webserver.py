import socket
from workerthread import WorkerThread

PORT = 8080

class WebServer:
    """
    サーバーを表すクラス
    """
    def serve(self):
        """
        サーバーを起動する
        """
        print("=== Server: サーバーを起動します ===")
        
        try:
            # socketを生成
            server_socket = self.create_server_socket()
            
            while True:
                # 外部からの接続を待ち、接続があったらコネクションを確立する
                print("=== Server: クライアントからの接続を待ちます ===")
                (client_socket, address) = server_socket.accept() # type: ignore
                print(f"=== Server: クライアントと接続しました remote_address: {address} ===")
                
                # クライアントを処理するスレッドを作成
                thread = WorkerThread(client_socket, address)
                # スレッドを実行
                thread.start()
            
        finally:
            print("=== Server: サーバーを停止します。 ===")
            
    def create_server_socket(self) -> socket: # type: ignore
        """
        通信を待ち受けるためのserver_socketを生成する
        :return:
        """
        # socketの生成
        server_socket = socket.socket()
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # socketをlocalhostのポートを割り当てる
        server_socket.bind(("localhost", PORT))
        server_socket.listen(10)
        return server_socket # type: ignore
