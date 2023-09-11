import requests
import csv

with open("testNew_17.csv", "rb") as f:
    csv_file = f.read()

url = "http://10.10.210.87/upload/complete/"

#name、filename、Content-Typeを指定 
files = {'file': ('testNew_17.csv', csv_file, "text/html")}

#nameとfilenameに同じ値を指定する場合 =>  files = {'file': tar_data}
#nameとfilenameをそれぞれ指定する場合 =>  files = {'file': ('test.tgz', tar_data)}

headers = {'Cookie': 'JSESSIONID=xxxxxxx;'}
req = requests.post(url=url, files=files, headers=headers)

print(req.headers)
print(req.text)