from flask import Flask, request
import sqlite3

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_datebase(querry):
    conn = sqlite3.connect('db1.db')
    conn.row_factory = dict_factory
    cursor = conn.execute(querry)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result


def gett_datebase(querry):
    with sqlite3.connect('db1.db') as conn:
        cursor = conn.cursor()
        cursor.execute(querry)
        conn.commit()


@app.route("/", methods=['GET'])  # Основная страница обменника
def hello():
    return "Hello everyone, you are on the currency exchanger!"


@app.get('/currency')  # Вывод всех валют
def list_of_currency():
    rez = get_datebase('select name, available_quantity, value_to_usd,'
                       ' date from Currency ')
    return rez


@app.get('/currency/<currency_name>')  # Вывод выбранной валюты
def name_of_currency(currency_name):
    rez = get_datebase(f'select name, available_quantity, value_to_usd, date '
                       f'from Currency where name="{currency_name}"')
    return rez


@app.get('/currency/<currency_name>/rating')  # Вывод рейтинга выбранной валюты
def ratings(currency_name):
    rez = get_datebase(f"""select cur_name, avg(rating) from 
    Rating where cur_name='{currency_name}' """)
    return rez


@app.get('/currency/rating')  # Вывод рейтинга всех валют
def rating_all():
    rez = get_datebase(f'select cur_name, avg(rating), comment from Rating '
                       f'Group by cur_name')
    return rez


# Вывод курса валюты относильно другой валюты
@app.get('/currency/trade/<currency_name1>/<currency_name2>')
def show_trade(currency_name1, currency_name2):
    rez = get_datebase(f"""select round((select value_to_usd from Currency 
    Where name='{currency_name1}' ORDER by date DESC limit 1)/ (select value_to_usd from Currency 
    Where name='{currency_name2}' ORDER by date DESC limit 1),
    2) as value_exchange""")
    return rez


@app.get('/user')  # Вывод баланса пользователя
def user_balance():
    rez = get_datebase(f'''Select Currency.name, Account.balance from Account
     JOIN Currency on Currency.id=Account.currency_id WHERE Account.user_id=1''')
    return rez


@app.get('/user/<user_id>/history')  # Вывод истории транзакций пользователя
def user_history(user_id):
    rez = get_datebase(f'''Select currency_transaction_in, currency_transaction_from, amount_spent_cur,
     amount_received_cur, date_time, commission from Trannsaction where 
     user_id='{user_id}' ''')
    return rez


@app.post('/currency/<currency_name>/rating')
def add_currency_rating(currency_name):
    request_data = request.get_json()
    comment = request_data['comment']
    rating = request_data['rating']
    gett_datebase(f"""Insert into Rating(cur_name, rating, comment) VALUES (
    '{currency_name}', {rating}, '{comment}')""")
    return 'ok'


#@app.post('/user/transfer')
#def user_transfer():
    #return f'Users transfer'


@app.post('/currency/trade/<currency_name1>/<currency_name2>')
def send_trade(currency_name1, currency_name2):
    user_id = 1



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
