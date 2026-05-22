import random
from typing import Callable

import pytest
from sqlalchemy.orm import Session

from src.main.api.classes.api_manager import ApiManager
from src.main.api.fixtures.user_fixture import FixtureData
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


class TestCreditRequest:

    @pytest.fixture
    def user_role(self):
        return dict(role='ROLE_CREDIT_SECRET')

    def test_credit_request(self, api_manager: ApiManager, request_credit_request: FixtureData, db_session: Session):
        response = api_manager.user_steps.request_credit(request_credit_request.user_request, request_credit_request.credit_request)

        assert request_credit_request.credit_request.term_months == response.term_months
        assert request_credit_request.credit_request.amount == response.balance

        credit_from_db = Credit.get_credit_by_id(db_session, credit_id=response.credit_id)
        assert credit_from_db.amount == response.balance
        assert credit_from_db.term_months == response.term_months

        transaction = Transaction.get_transaction_by_type(db_session, 'credit_issuance')
        assert request_credit_request.credit_request.account_id == transaction.to_account_id
        assert request_credit_request.credit_request.amount == transaction.amount




    @pytest.mark.parametrize("request_credit_request, response_spec", [
        ({'amount': random.randint(1, 5000)}, ResponseSpecs.request_bad()),
        ({'amount': random.randint(15001, 16000)}, ResponseSpecs.request_bad()),
        ({'amount': -1}, ResponseSpecs.request_bad()),
        ({'term_months': 0}, ResponseSpecs.request_bad()),
        ({'term_months': 61}, ResponseSpecs.request_bad()),
        ({'account_id': random.randint(1, 5000)}, ResponseSpecs.request_not_found()),
    ], indirect=['request_credit_request'])
    def test_credit_request_invalid(self, api_manager: ApiManager, request_credit_request: FixtureData, response_spec: Callable, db_session: Session):

        transaction_before = Transaction.get_transaction_by_type(db_session, 'credit_issuance')
        api_manager.user_steps.request_credit_bad(request_credit_request.user_request, request_credit_request.credit_request, response_spec=response_spec)

        transaction_after = Transaction.get_transaction_by_type(db_session, 'credit_issuance')
        assert transaction_before == transaction_after
