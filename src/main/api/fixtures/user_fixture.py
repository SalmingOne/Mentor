import pytest

from src.main.api.generators.model_generator import RandomModelGenerator
from src.main.api.models.create_user_request import CreateUserRequest
from mimesis import Person

from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest

person = Person()


class FixtureData:
    def __init__(self, *args, **kwargs):
        for item in args:
            if isinstance(item, FixtureData):
                for k,v in item.__dict__.items():
                    setattr(self, k, v)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __contains__(self, key):
        return key in self.__dict__

    def __iter__(self):
        return iter(self.__dict__.values())



@pytest.fixture
def user_role():
    return {}

@pytest.fixture
def create_user(api_manager, user_role, request):
    overrides = getattr(request, 'param', {})
    user_request = RandomModelGenerator.generate(CreateUserRequest, **user_role, **overrides)
    api_manager.admin_steps.create_user(user_request)
    return FixtureData(user_request=user_request)


@pytest.fixture
def create_account_factory(api_manager, create_user):
    def factory():
        response = api_manager.user_steps.create_bank_account(create_user.user_request)
        return FixtureData(create_user, account_response=response)

    return factory


@pytest.fixture
def create_account(create_account_factory):
    return create_account_factory()


@pytest.fixture
def deposit_account_request(api_manager, create_account, request):
    overrides = dict(
        account_id=create_account.account_response.id
    ) | getattr(request, 'param', {})
    deposit_account_request = RandomModelGenerator.generate(DepositAccountRequest, **overrides)
    return FixtureData(create_account, deposit_request=deposit_account_request)


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

    return FixtureData(account_a=a_response, transfer_request=transfer_account_request, user_request=create_user_request)


@pytest.fixture
def transfer_same_user(api_manager, create_user, request):
    param = getattr(request, 'param', {})
    a_response = api_manager.user_steps.create_bank_account(create_user.user_request)
    if param.pop('same_account_id', False):
        b_response = a_response
    else:
        b_response = api_manager.user_steps.create_bank_account(create_user.user_request)
    return _build_transfer_request(api_manager, create_user.user_request, a_response, b_response, param)

@pytest.fixture
def transfer_different_users(api_manager, create_account_factory, request):
    first_factory = create_account_factory()
    second_factory = create_account_factory()
    return _build_transfer_request(api_manager, first_factory.user_request, first_factory.account_response, second_factory.account_response, getattr(request, 'param', {}))



@pytest.fixture
def request_credit_request(api_manager, create_account, request):
    create_user_request, create_account_response = create_account
    overrides = dict(
        account_id=create_account_response.id
    ) | getattr(request, 'param', {})
    request_credit_request = RandomModelGenerator.generate(RequestCreditRequest, **overrides)
    return FixtureData(create_account, credit_request=request_credit_request)

@pytest.fixture
def repay_credit_request(api_manager, request_credit_request, request):
    credit_response = api_manager.user_steps.request_credit(request_credit_request.user_request, request_credit_request.credit_request)

    overrides = dict(
        account_id=request_credit_request.account_response.id,
        credit_id=credit_response.credit_id,
        amount=credit_response.amount,
    ) | getattr(request, 'param', {})

    repay_credit_request = RandomModelGenerator.generate(RepayCreditRequest, **overrides)

    return FixtureData(request_credit_request, repay_request=repay_credit_request)