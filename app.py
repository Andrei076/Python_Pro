from flask import Flask, request
import sqlite3
#from datetime import datetime
app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_database(querry):
    with sqlite3.connect('db1.db') as conn:
        conn.row_factory = dict_factory
        cursor = conn.execute(querry)
        result = cursor.fetchall()
        conn.commit()
        return result


@app.route("/", methods=['GET'])  # Основная страница обменника
def hello():
    return "Hello everyone, you are on the currency exchanger!"


@app.get('/currency')  # Вывод всех валют
def list_of_currency():
    rez = get_database('select name, available_quantity, value_to_usd,'
                       ' date from Currency ')
    return rez


@app.get('/currency/<currency_name>')  # Вывод выбранной валюты
def name_of_currency(currency_name):
    rez = get_database(f'select name, available_quantity, value_to_usd, date '
                       f'from Currency where name="{currency_name}"')
    return rez


@app.get('/currency/<currency_name>/rating')  # Вывод рейтинга выбранной валюты
def ratings(currency_name):
    rez = get_database(f"""select cur_name, round(avg(rating),1) as rating, 
    comment from 
    Rating where cur_name='{currency_name}' """)
    return rez


@app.get('/currency/rating')  # Вывод рейтинга всех валют
def rating_all():
    rez = get_database(f'select cur_name, round(avg(rating),1) as rating, '
                       f'comment from '
                       f'Rating '
                       f'Group by cur_name')
    return rez


# Вывод курса валюты относильно другой валюты
@app.get('/currency/trade/<currency_name1>/<currency_name2>')
def show_trade(currency_name1, currency_name2):
    rez = get_database(f"""select round((select value_to_usd from Currency 
    Where name='{currency_name1}' ORDER by date DESC limit 1)/ 
    (select value_to_usd from Currency 
    Where name='{currency_name2}' ORDER by date DESC limit 1),
    2) as value_exchange""")
    return rez


@app.get('/user')  # Вывод баланса пользователя
def user_balancee():
    rez = get_database(f'''Select Currency.name, Account.balance from Account
     JOIN Currency on Currency.id=Account.currency_id WHERE
      Account.user_id=1''')
    return rez


@app.get('/user/<user_id>/history')  # Вывод истории транзакций пользователя
def user_history(user_id):
    rez = get_database(f'''Select currency_transaction_in, 
    currency_transaction_from, amount_spent_cur,
     amount_received_cur, date_time, commission from Trannsaction where 
     user_id='{user_id}' ''')
    return rez


@app.post('/currency/<currency_name>/rating')
def add_currency_rating(currency_name):
    request_data = request.get_json()
    comment = request_data['comment']
    rating = request_data['rating']
    get_database(f"""Insert into Rating(cur_name, rating, comment) VALUES (
    '{currency_name}', {rating}, '{comment}')""")
    return 'ok'


@app.post('/currency/trade/<currency_name1>/<currency_name2>')
def send_trade(currency_name1, currency_name2):
    user_id = 1
    date = "11-10-2022"
    amount1 = request.get_json()["amount"]

    user_balance1 = get_database(f"""SELECT * from Account where
        user_id ='{user_id}' and name = '{currency_name1}'""")
    user_balance2 = get_database(f"""SELECT * from Account where
    user_id ='{user_id}' and name = '{currency_name2}'""")

    act_currency1 = get_database(f"""SELECT * from Currency where name=
      '{currency_name1}' ORDER by date DESC limit 1""")
    cur1_cost_to_one_usd = act_currency1[0]['value_to_usd']
    act_currency2 = get_database(f"""SELECT * from Currency where name=
    '{currency_name2}' ORDER by date DESC limit 1""")
    cur2_cost_to_one_usd = act_currency2[0]['value_to_usd']

    need_cur2 = amount1 * 1.0 * cur1_cost_to_one_usd / cur2_cost_to_one_usd

    exists_amount_currency2 = act_currency2[0]['available_quantity']

    if  (user_balance1[0]['balance'] >= amount1) and (exists_amount_currency2 >
                                                    need_cur2):
        get_database(f"update Currency set available_quantity = "
                     f"{exists_amount_currency2 - need_cur2} where date"
                     f"={act_currency2[0]['date']} and name ='{currency_name2}'")
        get_database(f"update Currency set available_quantity = "
                     f"{act_currency1[0]['available_quantity'] + amount1} "
                     f"where date ="
                     f" {act_currency2[0]['date']} and name = '{currency_name1}'")
        get_database(f"update Account set balance = "
                     f"{user_balance1[0]['balance']-amount1} where user_id "
                     f"={user_id} "
                     f"and name = '{currency_name1}'")
        get_database(f"update Account set balance = "
                     f"{user_balance2[0]['balance']+need_cur2} where user_id ="
                     f"{user_id} "
                     f"and name = '{currency_name2}'")
        get_database(f"""Insert into Trannsaction (user_id, type_transaction,
         amount_spent_cur, amount_received_cur, currency_transaction_in,
          currency_transaction_from, date_time, commission,
           balance_transaction_in, balance_transaction_from) Values (
'{user_id}', 'exchange', '{amount1}', {need_cur2}, '{currency_name2}', 
'{currency_name1}', '{date}', 0, {user_balance1[0]['id']}, 
{user_balance2[0]['id']})""")
        return 'successful operation'
    else:
        return 'Error. Something went wrong'


if __name__ == '__main__':
    app.run(debug=True)


# @app.get('/user/deposit/<deposit_id>')
# def user_deposit_id(deposit_id):
#     return f'Users deposit: {deposit_id}'
#
#
# @app.get('/deposit/<currency_name>')
# def deposit_currency_name(currency_name):
#     return 'deposit in : {currency_name}'
#
#
# @app.route('/user/deposit', methods=['GET', 'POST'])
# def user_deposit():
#     if request.method == 'GET':
#         return f'Information about users deposit'
#     else:
#         return f'Send deposit'

# @app.post('/user/transfer')
# def user_transfer():
# return f'Users transfer'
