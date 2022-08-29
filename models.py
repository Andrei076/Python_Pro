from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Account(db.Model):
    __tablename__ = "Account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    balance = db.Column(db.REAL, nullable=False)
    name = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'name': self.name
        }


class Currency(db.Model):
    __tablename__ = "Currency"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True,
                   nullable=False, unique=True)
    name = db.Column(db.String(20), nullable=False)
    value_to_usd = db.Column(db.REAL, nullable=False)
    available_quantity = db.Column(db.REAL, nullable=False)
    date = db.Column(db.String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value_to_usd': self.value_to_usd,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Rating(db.Model):
    __tablename__ = "Rating"

    id = db.Column(db.Integer, nullable=False, primary_key=True,
                   autoincrement=True, unique=True)
    cur_name = db.Column(db.String(30), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'cur_name': self.cur_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Trannsaction(db.Model):
    __tablename__ = "Trannsaction"

    id = db.Column(db.Integer, nullable=False, primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    type_transaction = db.Column(db.String(30), nullable=False)
    amount_spent_cur = db.Column(db.REAL, nullable=False)
    amount_received_cur = db.Column(db.REAL, nullable=False)
    currency_transaction_in = db.Column(db.String(30), nullable=False)
    currency_transaction_from = db.Column(db.String(30), nullable=False)
    date_time = db.Column(db.String(30), nullable=False)
    commission = db.Column(db.REAL, nullable=False)
    balance_transaction_in = db.Column(db.String, nullable=False)
    balance_transaction_from = db.Column(db.String, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'type_transaction': self.type_transaction,
            'amount_spent_cur': self. amount_spent_cur,
            'amount_received_cur': self.amount_received_cur,
            'currency_transaction_in': self.currency_transaction_in,
            'currency_transaction_from': self.currency_transaction_from,
            'date_time': self.date_time,
            'commission': self.commission,
            'balance_transaction_in': self.balance_transaction_in,
            'balance_transaction_from': self.balance_transaction_from
        }


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    login = db.Column(db.TEXT, nullable=False, unique=True)
    password = db.Column(db.TEXT, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }
