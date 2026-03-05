from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    currency: str = "USD"
    merchant_id: str
    timestamp: datetime
    location: Optional[str] = "USA"