from pydantic import BaseModel
from datetime import date


class Oferta(BaseModel):
    data_oferta: date
    produto_id: str
    quantidade: int
    valor_total: float
