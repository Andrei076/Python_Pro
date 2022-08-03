from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route('/currency/<currency_name>/review', methods=['GET', 'POST', 'PUT',
                                                        'DELETE'])
def review(currency_name):
    if request.method == 'GET':
        return f'List of review: {currency_name}'
    elif request.method == 'POST':
        return f'Send review: {currency_name}'
    elif request.method == 'PUT':
        return f'Change review: {currency_name}'
    elif request.method == 'DELETE':
        return f'Delete review: {currency_name}'


@app.get('/currency/<currency_name>')
def name_of_currency(currency_name):
    return f'Name of currency: {currency_name}'


@app.get('/currency')
def list_of_currency():
    return f'List of currency'


@app.get('/currency/trade/<currency_name1>/<currency_name2>')
def show_trade(currency_name1, currency_name2):
    return f'Exchange: {currency_name1} to {currency_name2}'


@app.post('/currency/trade/<currency_name1>/<currency_name2>')
def send_trade(currency_name1, currency_name2):
    return f'Exchange: {currency_name1} to {currency_name2}'


@app.get('/user')
def user_information():
    return f'Information about user'


@app.post('/user/transfer')
def user_transfer():
    return f'Users transfer'


@app.get('/user/history')
def user_history():
    return f'Information about users transfer'


@app.route('/user/deposit', methods=['GET', 'POST'])
def user_deposit():
    if request.method == 'GET':
        return f'Information about users deposit'
    else:
        return f'Send deposit'


@app.get('/user/deposit/<deposit_id>')
def user_deposit_id(deposit_id):
    return f'Users deposit: {deposit_id}'


@app.get('/deposit/<currency_name>')
def deposit_currency_name(currency_name):
    return f'deposit in : {currency_name}'
