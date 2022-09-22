from celery import Celery
import models
import database

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def task1(user_id, currency_name1, currency_name2, amount1, transaction_id):

    user_id = 1
    date = "22-09-2022"

    database.init_db()
    transaction_record = models.TransactionQueue.query.filter_by(
        transaction_id=transaction_id).first()
    user_balance1 = models.Account.query.filter_by(user_id=user_id,
                                            name=currency_name1).first()
    user_balance2 = models.Account.query.filter_by(user_id=user_id,
                                            name=currency_name2).first()


    act_currency1 = models.Currency.query.filter_by(
        name=currency_name1).order_by(
        models.Currency.date.desc()).first()
    cur1_cost_to_one_usd = act_currency1.value_to_usd

    act_currency2 = models.Currency.query.filter_by(
        name=currency_name2).order_by(
        models.Currency.date.desc()).first()
    cur2_cost_to_one_usd = act_currency2.value_to_usd

    need_cur2 = amount1 * 1.0 * cur1_cost_to_one_usd / cur2_cost_to_one_usd

    exists_amount_currency2 = act_currency2.available_quantity

    if (user_balance1.balance >= amount1) and (exists_amount_currency2 >
                                               need_cur2):

        models.Currency.query.filter_by(name=currency_name2,
                                 date=act_currency1.date).update(
            dict(available_quantity=(exists_amount_currency2 - need_cur2)))

        models.Currency.query.filter_by(name=currency_name1,
                                 date=act_currency2.date).update(
            dict(available_quantity=(act_currency1.available_quantity +
                                     amount1)))

        models.Account.query.filter_by(user_id=user_id, name=currency_name1).update(
            dict(balance=(user_balance1.balance - amount1)))

        models.Account.query.filter_by(user_id=user_id,
                                       name=currency_name2).update(
            dict(balance=(user_balance2.balance + need_cur2)))

        obj = models.Trannsaction(user_id=user_id, type_transaction='exchange',
                           amount_spent_cur=amount1,
                           amount_received_cur=need_cur2,
                           currency_transaction_from=currency_name1,
                           currency_transaction_in=currency_name2,
                           date_time=date, commission=0,
                           balance_transaction_in=user_balance1.id,
                           balance_transaction_from=user_balance2.id)
        database.db_session.add(obj)
        transaction_record.status ='done'
        database.db_session.add(transaction_record)
        database.db_session.commit()
        return 'successful operation'
    else:
        transaction_record.status = 'eror'
        database.db_session.add(transaction_record)
        database.db_session.commit()
        return 'Error. Something went wrong'
