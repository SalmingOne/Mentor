from sqlalchemy.orm import Session

from src.main.api.db.models.transaction_table import Transaction


class TransactionCrudDb:

    @staticmethod
    def get_transaction_by_type(db: Session, transaction_type: str) -> Transaction | None:
        return db.query(Transaction).filter(Transaction.transaction_type == transaction_type).order_by(Transaction.id.desc()).first()