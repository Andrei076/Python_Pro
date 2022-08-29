import requests


def post_rating():
    URL = 'http://127.0.0.1:5000/currency/KZT/rating'
    HEADERS = {'content-type': 'application/json'}
    data = {"cur_name": "KZT", "rating": 3, "comment":
        "not bad"}
    request_data = requests.post(URL, headers=HEADERS, json=data)
    print(request_data.text)


def post_trade():
    URL = 'http://127.0.0.1:5000/currency/trade/usd/uah'
    HEADERS = {'content-type': 'application/json'}
    data = {"amount": 10.0}
    request_data = requests.post(URL, headers=HEADERS, json=data)
    print(request_data.text)


if __name__ == "__main__":
    post_rating()
