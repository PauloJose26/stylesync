from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class Produto(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    nome: str
    preco: float
    estoque: int
    descricao: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )