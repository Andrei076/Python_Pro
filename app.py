from flask import Flask, request
import sqlite3
import sqlalchemy
import celery_worker
import database
import uuid
import models
from models import Currency, Account, Rating, Trannsaction
from celery_worker import task1
import database

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
    database.init_db()
    list_currency = Currency.query.all()
    return [item.to_dict() for item in list_currency]


@app.get('/currency/<currency_name>')  # Вывод выбранной валюты
def name_of_currency(currency_name):
    database.init_db()
    result = Currency.query.filter_by(name=currency_name).all()
    return [item.to_dict() for item in result]


@app.get('/currency/<currency_name>/rating')  # Вывод среднего рейтинга
# выбранной валюты
def ratings(currency_name):
    database.init_db()
    cur_rating = dict(database.db_session.query(sqlalchemy.func.avg(
        Rating.rating).label(
        f'average rating {currency_name}')).filter(Rating.cur_name ==
                                                   currency_name).first())
    return cur_rating


@app.get('/currency/review')  # Вывод рейтинга всех валют
def rating_all():
    database.init_db()
    review_all_currencies = Rating.query.all()
    return [item.to_dict() for item in review_all_currencies]


# Вывод курса валюты относильно другой валюты
@app.get('/currency/trade/<currency_name1>/<currency_name2>')
def show_trade(currency_name1, currency_name2):
    database.init_db()
    first_cur = Currency.query.filter_by(name=currency_name1).order_by(
        Currency.date.desc()).first()
    second_cur = Currency.query.filter_by(name=currency_name2).order_by(
        Currency.date.desc()).first()
    rez = round(first_cur.value_to_usd / second_cur.value_to_usd, 2)
    return f'{currency_name1} exchange to {currency_name2} = {rez}'


@app.get('/user')  # Вывод баланса пользователя
def user_balancee():
    database.init_db()
    balances = Account.query.filter_by(user_id=1)
    return [item.to_dict() for item in balances]


@app.get('/user/<user_id>/history')  # Вывод истории транзакций пользователя
def user_history(user_id):
    database.init_db()
    history_tran = Trannsaction.query.filter_by(user_id=user_id).all()
    return [item.to_dict() for item in history_tran]


@app.post('/currency/<currency_name>/rating')
def add_currency_rating(currency_name):
    database.init_db()
    request_data = request.get_json()
    comment = request_data['comment']
    rating = request_data['rating']
    obj = Rating(cur_name=currency_name, rating=rating, comment=comment)
    database.db_session.add(obj)
    database.db_session.commit()
    return 'ok'



@app.get('/test1')
def test1():
    task_obj = task1.apply_async(args=[1, 10, 20, 300])
    return str(task_obj)


@app.post('/currency/trade/<currency_name1>/<currency_name2>')
def send_trade(currency_name1, currency_name2):
    user_id = 1
    amount1 = request.get_json()["amount"]

    transaction_id = uuid.uuid4()
    database.init_db()
    transaction_queue_record = models.TransactionQueue(transaction_id=str(
        transaction_id), status='in queue')
    database.db_session.add(transaction_queue_record)
    database.db_session.commit()


    task_obj = task1.apply_async(args=[user_id, currency_name1,
                                       currency_name2, amount1, transaction_id])
    return {'task_id':str(task_obj)}



@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
