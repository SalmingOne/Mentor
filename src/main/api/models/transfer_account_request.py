from typing import Annotated

from pydantic import Field

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class TransferAccountRequest(BaseModel):
    from_account_id: int = Field(serialization_alias='fromAccountId')
    to_account_id: int = Field(serialization_alias='toAccountId')
    amount: Annotated[int, CreationRule(regex=r'^(50[0-9]|5[1-9][0-9]|[6-9][0-9]{2}|[1-9][0-9]{3}|10000)$')]