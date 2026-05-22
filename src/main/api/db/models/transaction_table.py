from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from src.main.api.db.base import Base


class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    to_account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=False)
    from_account_id = Column(Integer, ForeignKey('account.id', ondelete='CASCADE'), nullable=True)
    credit_id = Column(Integer, ForeignKey('credit.id'), nullable=True)
    amount = Column(Integer, nullable=False)
    transaction_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=True)