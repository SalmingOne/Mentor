from typing import Protocol, Optional

from requests import Response

from src.main.api.models.base_model import BaseModel


class CrudEndpoint(Protocol):

    def post(self, model: Optional[BaseModel]) -> BaseModel | Response: ...

    def put(self, user_id: int, model: Optional[BaseModel]) -> BaseModel | Response: ...

    def delete(self, user_id: int) -> BaseModel | Response: ...

    def patch(self, user_id: int, model: Optional[BaseModel]) -> BaseModel | Response: ...

    def get(self, user_id: int) -> BaseModel | Response: ...