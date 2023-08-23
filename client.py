import requests

#ログインに必要な情報
#重要①：URLに「?next=アクセスしたいページ」の部分を含めてはいけない。
URL = "http://10.10.210.87/"
ID = "admin.fujico@kfjc.co.jp" 	#"ログインするユーザのID"
PASS = "adminpassword"	#"ログインするユーザのパスワード"
NEXT = "index.html"	#"アクセスしたいページ"

#重要②：まずログインページにアクセスしてクッキーからtokenを取得する
session = requests.session()
res = session.get(URL)
csrf = session.cookies['csrftoken']

login_info = {
        "csrfmiddlewaretoken" : csrf,
        "username" : ID,
        "password" : PASS,
        "next" : NEXT,
        }

#重要③：headerにURLを渡す。
response = session.post(URL, data=login_info, headers=dict(Referer=URL))

