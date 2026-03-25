from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.main.api.db.base import Base
from src.main.api.db.models.transaction_table import Transaction


class Credit(Base):
    __tablename__ = 'credit'
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    amount = Column(Integer, nullable=False)
    term_months = Column(Integer, nullable=False)
    balance = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=True)

    transaction = relationship("Transaction", backref='transaction_credit', passive_deletes=True)
