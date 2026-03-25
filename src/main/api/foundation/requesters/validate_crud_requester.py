from typing import Callable, Optional

import allure

from src.main.api.configs.config import Config
from src.main.api.foundation.endpoint import Endpoint
from src.main.api.foundation.http_requester import HttpRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.base_model import BaseModel


class ValidateCrudRequester(HttpRequester):

    def __init__(self, request_spec: dict[str, str], response_spec: Callable, endpoint: Endpoint):
        super().__init__(request_spec, response_spec, endpoint)
        self.crud_requester = CrudRequester(request_spec=self.request_spec, response_spec=self.response_spec,
                                            endpoint=self.endpoint)

    def post(self, model: Optional[BaseModel] = None) -> BaseModel:
        response = self.crud_requester.post(model)

        with allure.step(f'POST {Config.fetch('urlBackend')}{self.endpoint.value.url} and Validated Model'):
            allure.attach(f'Validated Model response: {self.endpoint.value.response_model.__name__}',)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())

    def delete(self, user_id: int) -> BaseModel:
        response = self.crud_requester.delete(user_id)
        self.response_spec(response)
        return self.endpoint.value.response_model.model_validate(response.json())
