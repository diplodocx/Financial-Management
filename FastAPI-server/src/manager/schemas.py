from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class PaymentTypes(Enum):
    receiving = "receiving"
    spending = "spending"


class PaymentMethods(Enum):
    RUB = "RUB"


class CategoryGet(BaseModel):
    category_id: int
    category_name: str
    payment_type: PaymentTypes


class PaymentGet(BaseModel):
    payment_id: int
    payment_time: datetime
    amount: float
    method: PaymentMethods
    comment: str
    owner: int
    category_id: int
    category_name: str
    payment_type: PaymentTypes


class PaymentPost(BaseModel):
    amount: float
    method: PaymentMethods
    comment: Optional[str]
    owner: int
    category: int
