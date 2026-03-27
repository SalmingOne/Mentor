from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb
from src.main.api.fixtures.user_fixture import FixtureData


class TestCreateAccount:
    def test_create_account(self, api_manager: ApiManager, create_user: FixtureData, db_session: Session) -> None:
        response = api_manager.user_steps.create_bank_account(create_user.user_request)
        assert 0 == response.balance

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id




