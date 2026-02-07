from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from bson import ObjectId


class LoginPayload(BaseModel):
    username: str
    password: str


class UsuarioBase(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    