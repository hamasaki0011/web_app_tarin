import requests

URL = "http://10.10.210.87/"
ID = "admin.fujico@kfjc.co.jp"  #"ログインするユーザのID"
PASS = "adminpassword"  #"ログインするユーザのパスワード"
NEXT = "index.html" #"アクセスしたいページ"

session = requests.session()
res = session.get(URL)
csrf = session.cookies['csrftoken']
 
data = {     
        "csrfmiddlewaretoken" : csrf,
        "next" : NEXT,
        }
 
response = session.post(URL, data=data, headers=dict(Referer=URL))

print(response)