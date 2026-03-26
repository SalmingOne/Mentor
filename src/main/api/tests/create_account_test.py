from src.main.api.db.crud.account_crud import AccountCrudDb as Account, AccountCrudDb


class TestCreateAccount:
    def test_create_account(self, api_manager, create_user, db_session):
        response = api_manager.user_steps.create_bank_account(create_user)
        assert 0 == response.balance

        account_from_db = AccountCrudDb.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id




