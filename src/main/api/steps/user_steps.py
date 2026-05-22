from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.models.base_model import BaseModel
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.repay_credit_request import RepayCreditRequest
from src.main.api.models.request_credit_request import RequestCreditRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps


class UserSteps(BaseSteps):

    def create_bank_account(self, create_user_request: CreateUserRequest) -> BaseModel:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.CREATE_ACCOUNT
        ).post()
        return response


    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest) -> BaseModel:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.DEPOSIT_ACCOUNT
        ).post(deposit_account_request)

        return response


    def deposit_account_bad(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest, response_spec=ResponseSpecs.request_bad()) -> None:
        CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            response_spec=response_spec,
            endpoint=Endpoint.DEPOSIT_ACCOUNT
        ).post(deposit_account_request)

    def transfer_account(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest) -> BaseModel:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,
                                                   password=create_user_request.password),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.TRANSFER_ACCOUNT
        ).post(transfer_account_request)

        return response

    def transfer_account_bad(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest, response_spec=ResponseSpecs.request_bad()) -> None:
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,
                                                   password=create_user_request.password),
            response_spec=response_spec,
            endpoint=Endpoint.TRANSFER_ACCOUNT
        ).post(transfer_account_request)

    def request_credit(self, create_user_request: CreateUserRequest, request_credit_request: RequestCreditRequest) -> BaseModel:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            response_spec=ResponseSpecs.request_created(),
            endpoint=Endpoint.REQUEST_CREDIT
        ).post(request_credit_request)

        return response

    def request_credit_bad(self, create_user_request: CreateUserRequest, request_credit_request: RequestCreditRequest, response_spec=ResponseSpecs.request_bad()) -> None:
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,password=create_user_request.password),
            response_spec=response_spec,
            endpoint=Endpoint.REQUEST_CREDIT
        ).post(request_credit_request)


    def repay_credit(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest) -> BaseModel:
        response = ValidateCrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,
                                                   password=create_user_request.password),
            response_spec=ResponseSpecs.request_ok(),
            endpoint=Endpoint.REPAY_CREDIT
        ).post(repay_credit_request)

        return response

    def repay_credit_bad(self, create_user_request: CreateUserRequest, repay_credit_request: RepayCreditRequest, response_spec=ResponseSpecs.request_bad()) -> None:
        response = CrudRequester(
            request_spec=RequestSpecs.auth_headers(username=create_user_request.username,
                                                   password=create_user_request.password),
            response_spec=response_spec,
            endpoint=Endpoint.REPAY_CREDIT
        ).post(repay_credit_request)

