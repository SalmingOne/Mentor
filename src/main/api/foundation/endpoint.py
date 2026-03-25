from dataclasses import dataclass
from enum import Enum
from typing import Optional, Type

from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.repay_credit_response import RepayCreditResponse
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.request_credit_response import RequestCreditResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        request_model=CreateUserRequest,
        response_model=CreateUserResponse,
        url='/admin/create'
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        request_model=None,
        response_model=None,
        url='/admin/users'
    )

    LOGIN_USER = EndpointConfiguration(
        request_model=LoginUserRequest,
        response_model=LoginUserResponse,
        url='/auth/token/login'
    )

    CREATE_ACCOUNT = EndpointConfiguration(
        request_model=None,
        response_model=CreateAccountResponse,
        url='/account/create'
    )
    DEPOSIT_ACCOUNT = EndpointConfiguration(
        request_model=DepositAccountRequest,
        response_model=DepositAccountResponse,
        url='/account/deposit'
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        request_model=TransferAccountRequest,
        response_model=TransferAccountResponse,
        url='/account/transfer'
    )

    REQUEST_CREDIT = EndpointConfiguration(
        request_model=RequestCreditRequest,
        response_model=RequestCreditResponse,
        url='/credit/request'
    )

    REPAY_CREDIT = EndpointConfiguration(
        request_model=RepayCreditRequest,
        response_model=RepayCreditResponse,
        url='/credit/repay'
    )