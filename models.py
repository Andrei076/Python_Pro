from sqlalchemy import Column, Integer, String, Text, REAL
from database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Account(Base):
    __tablename__ = "Account"

    id = Column(Integer, primary_key=True, autoincrement=True,
                   nullable=False, unique=True)
    user_id = Column(Integer, nullable=False)
    balance = Column(REAL, nullable=False)
    name = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'balance': self.balance,
            'name': self.name
        }


class Currency(Base):
    __tablename__ = "Currency"

    id = Column(Integer, primary_key=True, autoincrement=True,
                   nullable=False, unique=True)
    name = Column(String(20), nullable=False)
    value_to_usd = Column(REAL, nullable=False)
    available_quantity = Column(REAL, nullable=False)
    date = Column(String(20), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value_to_usd': self.value_to_usd,
            'available_quantity': self.available_quantity,
            'date': self.date
        }


class Rating(Base):
    __tablename__ = "Rating"

    id = Column(Integer, nullable=False, primary_key=True,
                   autoincrement=True, unique=True)
    cur_name = Column(String(30), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(30))

    def to_dict(self):
        return {
            'id': self.id,
            'cur_name': self.cur_name,
            'rating': self.rating,
            'comment': self.comment
        }


class Trannsaction(Base):
    __tablename__ = "Trannsaction"

    id = Column(Integer, nullable=False, primary_key=True,
                   autoincrement=True)
    user_id = Column(Integer, nullable=False)
    type_transaction = Column(String(30), nullable=False)
    amount_spent_cur = Column(REAL, nullable=False)
    amount_received_cur = Column(REAL, nullable=False)
    currency_transaction_in = Column(String(30), nullable=False)
    currency_transaction_from = Column(String(30), nullable=False)
    date_time = Column(String(30), nullable=False)
    commission = Column(REAL, nullable=False)
    balance_transaction_in = Column(String, nullable=False)
    balance_transaction_from = Column(String, nullable=False)

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


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'login': self.login,
            'password': self.password
        }


class TransactionQueue(Base):
    __tablename__ = "TransactionQueue"

    id = Column(Integer, primary_key=True, nullable=False)
    transaction_id = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
