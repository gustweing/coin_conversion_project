from pydantic import BaseModel, PositiveFloat
from datetime import datetime 

class ProductUpdate(BaseModel):
    code: str 
    codein: str
    max: PositiveFloat
    min: PositiveFloat
    bid: PositiveFloat
    time: datetime
