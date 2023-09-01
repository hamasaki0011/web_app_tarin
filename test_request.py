import requests
from requests.auth import HTTPBasicAuth

# 下記は、Basic認証の接続テストができるサイトです。
url = 'http://leggiero.sakura.ne.jp/xxxxbasic_auth_testxxxx/secret/kaiin_page_top.htm'
# ユーザー名を指定
username = 'kaiin'
# パスワードを指定
password = 'naisho'

# GET送信のケース
# response = requests.get(url, auth=requests.auth.HTTPBasicAuth(username, password))
# POST送信のケース
data = {'key1': 'value1'}
response = requests.post(url, data=data,auth=requests.auth.HTTPBasicAuth(username, password))
print(response)
print(response.text)
print(response.cookies)