import requests, json

end_point = "https://api.itc-app.site/api-practice/plus/"
headers = {"context-Type": "application/json"}

data = {
    "first_number": 5,
    "second_number": 10
}

def main():
    json_data = json.dumps(data)

    res = requests.post(end_point, data = json_data, headers = headers)

    print(res)
    print(res.text)
    print(type(res.text))

    res_json = json.loads(res.text)
    print(res_json)
    print(type(res_json))
    
if __name__ == "__main__":
    main()
