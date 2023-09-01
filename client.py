import requests

#ログインに必要な情報
#重要①：URLに「?next=アクセスしたいページ」の部分を含めてはいけない。
URL = "http://10.10.210.87/"
ID = "admin.fujico@kfjc.co.jp" 	#"ログインするユーザのID"
PASS = "adminpassword"	#"ログインするユーザのパスワード"
NEXT = "upload.html"	#"アクセスしたいページ"

# URL = "http://127.0.0.1:8080/login.html"
# ID = "TARO" 	#"ログインするユーザのID"
# #PASS = "adminpassword"	#"ログインするユーザのパスワード"
# NEXT = "index.html"	#"アクセスしたいページ"

#重要②：まずログインページにアクセスしてクッキーからtokenを取得する
session = requests.session()
res = session.get(URL)
csrf = session.cookies['csrftoken']

# print("session = ",session)
# print("res = ",res)
print("csrfを取得しました: ",csrf)

login_info = {
        "csrfmiddlewaretoken" : csrf,
        "email" : ID,
        # "username" : ID,
        "password" : PASS,
        "next" : NEXT,
        }

# print("ヘッダー: ", res.headers)
#重要③：headerにURLを渡す。
response = session.post(URL, data=login_info, headers=dict(Referer=URL))

print("ステータス", response)
# print("ヘッダー: ", response.headers)
print(response.headers['Content-Type'])
