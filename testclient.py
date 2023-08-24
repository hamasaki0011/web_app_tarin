import urllib.request

url = 'https://httpbin.org/get'
 
r = urllib.request.Request(url)
 
with urllib.request.urlopen(r) as response:
    body = response.read()
    print(body.decode('utf-8'))
    
# # レスポンスの内容を、ファイルに書き出す
# with open("test_client_recv.txt", "wb") as f:
#     f.write(body)