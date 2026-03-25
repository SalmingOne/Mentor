from sqlalchemy.orm import Session

from src.main.api.db.models.user_table import User


class UserCrudDb:
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter_by(id=user_id).first()

    @staticmethod
    def create_user(db: Session, username, password, role):
        user = User(username=username, password=password, role=role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(self, db: Session, user_id: int) -> None:
        user = db.query(User).filter_by(id=user_id).first()
        if user:
            db.delete(user)
            db.commit()

