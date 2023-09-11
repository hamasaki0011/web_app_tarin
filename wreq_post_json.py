import pprint
import json
import requests

def main():
    response = requests.post(
        'http://127.0.0.1:5000/post',
        json.dumps({'foo': 'bar'}),
        headers = {'Content-Type': 'application/json'}
    )
    
    pprint.pprint(response.json())


if __name__ == '__main__':
    main()