from flask import Flask
import sqlite3
app = Flask(__name__)


def get_db(querry):
    conn = sqlite3.connect('db1.db')
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.close()
    return result


@app.route("/")  # Основная страница обменника
def hello():
    return "Hello everyone, you are on the currency exchanger!"


@app.get('/currency')  # Вывод всех валют
def list_of_currency():
    rez = get_db('select * from Currency')
    return rez


@app.get('/currency/<currency_name>')  # Вывод выбранной валюты
def name_of_currency(currency_name):
    rez = get_db(f'select * from Currency where name="{currency_name}"')
    return rez


@app.get('/currency/<currency_name>/rating')  # Вывод рейтинга выбранной валюты
def rating(currency_name):
    rez = get_db(f'select avg(rating) from Rating where cur_name='
                 f'"{currency_name}"')
    return rez


@app.get('/currency/rating')  # Вывод рейтинга всех валют
def rating_all():
    rez = get_db(f'select avg(rating), cur_name from Rating Group by cur_name')
    return rez


# Вывод курса валюты относильно другой валюты
@app.get('/currency/trade/<currency_name1>/<currency_name2>')
def show_trade(currency_name1, currency_name2):
    rez = get_db(f'''select round((select value_to_usd from Currency Where 
    date='11-09-2022' and name='{currency_name1}')/ (select value_to_usd from Currency 
    Where date='11-09-2022' and name='{currency_name2}'),2)''')
    return rez


@app.get('/user')  # Вывод баланса пользователя
def user_balance():
    rez = get_db(f'''Select Currency.name, Account.balance from Account
     JOIN Currency on Currency.id=Account.currency_id WHERE Account.user_id=1''')
    return rez


@app.get('/user/<user_id>/history')  # Вывод истории транзакций пользователя
def user_history(user_id):
    rez = get_db(f'''Select currency_transaction_in, currency_transaction_from, amount_spent_cur,
     amount_received_cur, date_time, commission from Trannsaction where 
     user_id='{user_id}' ''')
    return rez


@app.post('/user/transfer')
def user_transfer():
    return f'Users transfer'


@app.post('/currency/trade/<currency_name1>/<currency_name2>')
def send_trade(currency_name1, currency_name2):
    return f'Exchange: {currency_name1} to {currency_name2}'


if __name__ == '__main__':
    app.run(debug=True)


# @app.get('/user/deposit/<deposit_id>')
# def user_deposit_id(deposit_id):
#     return f'Users deposit: {deposit_id}'
#
#
# @app.get('/deposit/<currency_name>')
# def deposit_currency_name(currency_name):
#     return f'deposit in : {currency_name}'
#
#
# @app.route('/user/deposit', methods=['GET', 'POST'])
# def user_deposit():
#     if request.method == 'GET':
#         return f'Information about users deposit'
#     else:
#         return f'Send deposit'
