from pydantic import Field

from src.main.api.models.base_model import BaseModel


class RepayCreditRequest(BaseModel):
    credit_id: int = Field(serialization_alias="creditId")
    account_id: int = Field(serialization_alias="accountId")
    amount: int