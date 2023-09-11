import pprint
# import json
import requests

def main():
    response = requests.get(
        'http://127.0.0.1:5000/get',
        params = {'foo': 'bar'}
    )
    
    pprint.pprint(response.json())
    
if __name__ == '__main__':
    main()