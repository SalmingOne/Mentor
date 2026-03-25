import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from mimesis import Person

from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest

person = Person()


@pytest.fixture
def user_role():
    return {}

@pytest.fixture
def create_user(api_manager, user_role, request):
    overrides = getattr(request, 'param', {})
    user_request = RandomModelGenerator.generate(CreateUserRequest, **user_role, **overrides)
    api_manager.admin_steps.create_user(user_request)
    return user_request


@pytest.fixture
def create_account_factory(api_manager, create_user):
    def factory():
        response = api_manager.user_steps.create_bank_account(create_user)
        return create_user, response

    return factory


@pytest.fixture
def create_account(create_account_factory):
    return create_account_factory()


@pytest.fixture
def deposit_account_request(api_manager, create_account, request):
    _, create_account_response = create_account
    overrides = dict(
        account_id=create_account_response.id
    ) | getattr(request, 'param', {})
    deposit_account_request = RandomModelGenerator.generate(DepositAccountRequest, **overrides)
    return deposit_account_request, create_account


def _build_transfer_request(api_manager, create_user_request, a_response, b_response, overrides):
    deposit_request = RandomModelGenerator.generate(DepositAccountRequest, account_id=a_response.id)
    deposit_request.amount = 9000

    api_manager.user_steps.deposit_account(create_user_request, deposit_request)
    deposit_response = api_manager.user_steps.deposit_account(create_user_request, deposit_request)  # второй раз пополняем

    transfer_account_request = RandomModelGenerator.generate(TransferAccountRequest, **dict(
        from_account_id=a_response.id,
        to_account_id=b_response.id,
    ) | overrides)

    a_response.balance = deposit_response.balance

    return transfer_account_request, create_user_request, a_response


@pytest.fixture
def transfer_same_user(api_manager, create_user, request):
    param = getattr(request, 'param', {})
    a_response = api_manager.user_steps.create_bank_account(create_user)
    if param.pop('same_account_id', False):
        b_response = a_response
    else:
        b_response = api_manager.user_steps.create_bank_account(create_user)
    return _build_transfer_request(api_manager, create_user, a_response, b_response, param)

@pytest.fixture
def transfer_different_users(api_manager, create_account_factory, request):
    create_user_request, response_a = create_account_factory()
    _, response_b = create_account_factory()
    return _build_transfer_request(api_manager, create_user_request, response_a, response_b, getattr(request, 'param', {}))



@pytest.fixture
def request_credit_request(api_manager, create_account, request):
    create_user_request, create_account_response = create_account
    overrides = dict(
        account_id=create_account_response.id
    ) | getattr(request, 'param', {})
    request_credit_request = RandomModelGenerator.generate(RequestCreditRequest, **overrides)
    return request_credit_request, create_account

@pytest.fixture
def repay_credit_request(api_manager, request_credit_request, request):
    request_credit_request_, (create_user_request, create_account_response) = request_credit_request
    credit_response = api_manager.user_steps.request_credit(create_user_request, request_credit_request_)

    overrides = dict(
        account_id=create_account_response.id,
        credit_id=credit_response.credit_id,
        amount=credit_response.amount,
    ) | getattr(request, 'param', {})

    repay_credit_request = RandomModelGenerator.generate(RepayCreditRequest, **overrides)

    return repay_credit_request, create_user_request