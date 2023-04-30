from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel


class PaymentTypes(Enum):
    receiving = "receiving"
    spending = "spending"


class CategoryGet(BaseModel):
    category_id: int
    category_name: str
    payment_type: PaymentTypes
