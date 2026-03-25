from typing import Annotated

from pydantic import Field

from src.main.api.generators.creation_rule import CreationRule
from src.main.api.models.base_model import BaseModel


class RequestCreditRequest(BaseModel):
    account_id: int = Field(serialization_alias='accountId')
    amount: Annotated[int, CreationRule(regex=r'^(500[0-9]|50[1-9][0-9]|5[1-9][0-9]{2}|[6-9][0-9]{3}|10000)$')]
    term_months: Annotated[int, CreationRule(regex=r'^([1-9]|[1-5][0-9]|60)$')] = Field(serialization_alias='termMonths')