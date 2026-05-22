import random
from typing import Callable

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixture import FixtureData
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestTransferAccount:

    def test_transfer_account(self, api_manager: ApiManager, transfer_same_user: FixtureData, db_session: Session):

        response = api_manager.user_steps.transfer_account(transfer_same_user.user_request, transfer_same_user.transfer_request)

        assert transfer_same_user.account_a.balance - transfer_same_user.transfer_request.amount == response.from_account_id_balance

        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'transfer')
        assert transfer_same_user.transfer_request.to_account_id == transaction_from_db.to_account_id
        assert transfer_same_user.transfer_request.from_account_id == transaction_from_db.from_account_id
        assert transfer_same_user.transfer_request.amount == transaction_from_db.amount


    def test_transfer_between_different_users(self, api_manager: ApiManager, transfer_different_users: FixtureData, db_session: Session):

        response = api_manager.user_steps.transfer_account(transfer_different_users.user_request, transfer_different_users.transfer_request)

        assert transfer_different_users.account_a.balance - transfer_different_users.transfer_request.amount == response.from_account_id_balance

        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'transfer')
        assert transfer_different_users.transfer_request.to_account_id == transaction_from_db.to_account_id
        assert transfer_different_users.transfer_request.from_account_id == transaction_from_db.from_account_id
        assert transfer_different_users.transfer_request.amount == transaction_from_db.amount

    @pytest.mark.parametrize("transfer_same_user, response_spec", [
        ({'amount': random.randint(1, 500)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(10001, 11000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'from_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'to_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'same_account_id': True}, ResponseSpecs.request_bad()),
    ], indirect=['transfer_same_user'])
    def test_transfer_account_invalid(self, api_manager: ApiManager, transfer_same_user: FixtureData, response_spec: Callable, db_session: Session):

        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'transfer')
        api_manager.user_steps.transfer_account_bad(transfer_same_user.user_request, transfer_same_user.transfer_request, response_spec=response_spec)
        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'transfer')

        assert transaction_from_db_before == transaction_from_db_after

    @pytest.mark.parametrize("transfer_different_users, response_spec", [
        ({'amount': random.randint(1, 500)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(10001, 11000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'from_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'to_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
    ], indirect=['transfer_different_users'])
    def test_transfer_between_different_users_invalid(self, api_manager: ApiManager, transfer_different_users: FixtureData, response_spec: Callable, db_session: Session):
        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'transfer')
        api_manager.user_steps.transfer_account_bad(transfer_different_users.user_request,
                                                    transfer_different_users.transfer_request, response_spec=response_spec)

        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'transfer')

        assert transaction_from_db_before == transaction_from_db_after





