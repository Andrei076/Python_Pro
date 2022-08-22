import requests


def post_rating():
    URL = 'http://127.0.0.1:5000/currency/Dollar/rating'
    HEADERS = {'content-type': 'application/json'}
    data = {"cur_name": "Dollar", "rating": 3, "comment":
        "not bad"}
    request_data = requests.post(URL, headers=HEADERS, json=data)
    print(request_data.text)



def post_trade():
    URL = 'http://127.0.0.1:5000/currency/trade/Usd/Eur'
    HEADERS = {'content-type': 'application/json'}
    data = {'data':
                {},
            'result': 'ok'
            }
    request_data = requests.post(URL, headers=HEADERS, json=data)
    print(request_data.text)

if __name__=="__main__":
    post_rating()