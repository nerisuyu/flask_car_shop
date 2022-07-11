import json
import requests

def __get_token():
    pass


def make_get_request(url,token):
    pass

if __name__ == '__main__':
    token = get_token(username='admin',password='admin')
    ####
    print('token', token)
    result = make_get_request("hhtp://127.0.0.1:5001/gey-money",token=token)
    print('result',json.loads(result))