import random

import pytest

from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.specs.response_specs import ResponseSpecs


class TestRepayCredit:

    @pytest.fixture
    def user_role(self):
        return dict(role='ROLE_CREDIT_SECRET')

    def test_repay_credit(self, api_manager, repay_credit_request, db_session):

        response = api_manager.user_steps.repay_credit(repay_credit_request.user_request, repay_credit_request.repay_request)

        assert repay_credit_request.repay_request.credit_id == response.credit_id
        assert repay_credit_request.repay_request.amount == response.amount_deposited
        transaction_from_db = Transaction.get_transaction_by_type(db_session, 'credit_repayment')

        assert repay_credit_request.repay_request.account_id == transaction_from_db.from_account_id
        assert repay_credit_request.repay_request.amount == transaction_from_db.amount

    @pytest.mark.parametrize("repay_credit_request, response_spec", [
        ({'amount': random.randint(1, 5000)}, ResponseSpecs.unprocessable_entity()),
        ({'amount': random.randint(15001, 16000)}, ResponseSpecs.unprocessable_entity()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'account_id': random.randint(1, 5000)}, ResponseSpecs.request_not_found()),
        ({'credit_id': random.randint(1, 5000)}, ResponseSpecs.request_not_found()),
    ], indirect=['repay_credit_request'])
    def test_repay_credit_invalid(self, api_manager, repay_credit_request, response_spec, db_session):
        transaction_from_db_before = Transaction.get_transaction_by_type(db_session, 'credit_repayment')

        api_manager.user_steps.repay_credit_bad(repay_credit_request.user_request, repay_credit_request.repay_request, response_spec)
        transaction_from_db_after = Transaction.get_transaction_by_type(db_session, 'credit_repayment')

        assert transaction_from_db_before == transaction_from_db_after
