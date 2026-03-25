import random

import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction


class TestDepositAccount:

    # def test_deposit_account(self, api_manager, create_account):
    #     create_user_request, create_account_response = create_account
    #     deposit_account_request = RandomModelGenerator.generate(DepositAccountRequest, account_id=create_account_response.id)
    #
    #     response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)
    #
    #     assert create_account_response.balance + deposit_account_request.amount == response.balance

    def test_deposit_account(self, api_manager, deposit_account_request, db_session):
        deposit_account_request, (create_user_request, create_account_response) = deposit_account_request

        response = api_manager.user_steps.deposit_account(create_user_request, deposit_account_request)

        assert create_account_response.balance + deposit_account_request.amount == response.balance

        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'deposit')
        assert deposit_account_request.account_id == transaction_from_db.to_account_id
        assert deposit_account_request.amount == transaction_from_db.amount

    @pytest.mark.parametrize("deposit_account_request, response_spec", [
        ({'amount': random.randint(1, 1000)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(9001, 10000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'account_id': random.randint(1, 10000)}, ResponseSpecs.request_not_found()),
    ], indirect=['deposit_account_request'])
    def test_deposit_deposit_invalid(self, api_manager, create_account, deposit_account_request, response_spec, db_session):
        deposit_account_request, (create_user_request, create_account_response) = deposit_account_request

        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'deposit')
        api_manager.user_steps.deposit_account_bad(create_user_request, deposit_account_request, response_spec=response_spec)

        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'deposit')
        assert transaction_from_db_before == transaction_from_db_after
