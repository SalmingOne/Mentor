import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:

    @staticmethod
    def base_headers() -> dict:
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }

    @staticmethod
    def auth_headers(username: str, password: str) -> dict:
        login_user_request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f'{Config.fetch('urlBackend')}/auth/token/login', headers=RequestSpecs.base_headers(),
            json=login_user_request.model_dump()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers['Authorization'] = f'Bearer {token}'
            return headers
        raise Exception('Invalid credentials')

    @staticmethod
    def unauth_headers() -> dict:
        return RequestSpecs.base_headers()