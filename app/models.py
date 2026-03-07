from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    currency: str = "USD"
    merchant_id: str
    timestamp: datetime
    location: Optional[str] = "USA"

# This represents the raw incoming data
class TransactionBase(SQLModel):
    transaction_id: str
    account_id: str
    amount: float
    currency: str = "USD"
    merchant_id: str
    timestamp: datetime
    location: Optional[str] = "USA"

# This represents what we save in the DB (includes our Fraud verdict)
class TransactionRecord(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_fraud: bool = False
    fraud_reason: Optional[str] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)