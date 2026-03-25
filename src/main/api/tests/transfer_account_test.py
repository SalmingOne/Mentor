import random

import pytest

from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestTransferAccount:

    def test_transfer_account(self, api_manager, transfer_same_user, db_session):
        transfer_account_request, create_user_request, account_a = transfer_same_user

        response = api_manager.user_steps.transfer_account(create_user_request, transfer_account_request)

        assert account_a.balance - transfer_account_request.amount == response.from_account_id_balance

        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'transfer')
        assert transfer_account_request.to_account_id == transaction_from_db.to_account_id
        assert transfer_account_request.from_account_id == transaction_from_db.from_account_id
        assert transfer_account_request.amount == transaction_from_db.amount


    def test_transfer_between_different_users(self, api_manager, transfer_different_users, db_session):
        transfer_account_request, create_user_request, account_a = transfer_different_users

        response = api_manager.user_steps.transfer_account(create_user_request, transfer_account_request)

        assert account_a.balance - transfer_account_request.amount == response.from_account_id_balance

        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'transfer')
        assert transfer_account_request.to_account_id == transaction_from_db.to_account_id
        assert transfer_account_request.from_account_id == transaction_from_db.from_account_id
        assert transfer_account_request.amount == transaction_from_db.amount

    @pytest.mark.parametrize("transfer_same_user, response_spec", [
        ({'amount': random.randint(1, 500)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(10001, 11000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'from_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'to_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'same_account_id': True}, ResponseSpecs.request_bad()),
    ], indirect=['transfer_same_user'])
    def test_transfer_account_invalid(self, api_manager, transfer_same_user, response_spec, db_session):
        transfer_account_request, create_user_request, account_a = transfer_same_user

        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'transfer')
        api_manager.user_steps.transfer_account_bad(create_user_request, transfer_account_request, response_spec=response_spec)
        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'transfer')

        assert transaction_from_db_before == transaction_from_db_after

    @pytest.mark.parametrize("transfer_different_users, response_spec", [
        ({'amount': random.randint(1, 500)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(10001, 11000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'from_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
        ({'to_account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
    ], indirect=['transfer_different_users'])
    def test_transfer_between_different_users_invalid(self, api_manager, transfer_different_users, response_spec, db_session):
        transfer_account_request, create_user_request, account_a = transfer_different_users

        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'transfer')
        api_manager.user_steps.transfer_account_bad(create_user_request, transfer_account_request,
                                                    response_spec=response_spec)
        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'transfer')

        assert transaction_from_db_before == transaction_from_db_after





