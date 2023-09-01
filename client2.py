import requests

URL = "http://10.10.210.87/"
ID = "admin.fujico@kfjc.co.jp" 	#"ログインするユーザのID"
PASS = "adminpassword"	#"ログインするユーザのパスワード"
NEXT = "index.html"	#"アクセスしたいページ"
#重要②：まずログインページにアクセスしてクッキーからtokenを取得する
session = requests.session()
res = session.post(URL)
# csrf = session.cookies['csrftoken']

print("res = ",res)
# print(res.text)
