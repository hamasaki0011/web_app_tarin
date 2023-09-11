import pprint
import requests

def main():
    response = requests.post(
        'http://127.0.0.1:5000/post',
        {'foo': 'bar'}
    )
    
    pprint.pprint(response.json())
    
if __name__ == '__main__':
    main()
    
