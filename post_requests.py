import requests


def post_rating():
    URL = 'http://127.0.0.1:5000/currency/Dollar/ratings'
    HEADERS = {'content-type': 'application/json'}
    data = {'data':
        {"cur_name": "Dollar","comment": "Perfect","rating": "7"},
        'result': 'ok'
    }
    req = requests.post(URL, headers=HEADERS, json=data)
    print(req.status_code, req.text)
