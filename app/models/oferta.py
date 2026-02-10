from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId
from datetime import date


class Oferta(BaseModel):
    data_oferta: date
    produto_id: str
    quantidade: int
    valor_total: float

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
