from typing import Annotated

from pydantic import Field

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class DepositAccountRequest(BaseModel):
    account_id: int = Field(serialization_alias='accountId')
    amount: Annotated[int, CreationRule(regex=r'^(?:9000|[1-8][0-9][0-9][0-9])$')]
