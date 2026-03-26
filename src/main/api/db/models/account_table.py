from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.main.api.db.base import Base


class Account(Base):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    number = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)

    credit = relationship("Credit", backref='account', passive_deletes=True)
    transaction_to = relationship("Transaction", backref='to_account', foreign_keys="Transaction.to_account_id", passive_deletes=True)
    transaction_from = relationship("Transaction", backref='from_account', foreign_keys="Transaction.from_account_id", passive_deletes=True)
