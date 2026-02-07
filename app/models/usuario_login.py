from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from bson import ObjectId

from app import db


class LoginPayload(BaseModel):
    username: str
    password: str


class UsuarioBase(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    username: str = Field(pattern=r"^[a-zA-Z]{1}[a-zA-Z0-9]+$")
    nome: str
    senha: str

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    @model_validator(mode="after")
    def verificar_se_username_ja_existe(self):
        usuario = db.usuarios.find_one({"username": self.username})
        if usuario:
            raise ValueError("Usuário com esse username já existe")
        return self


class UsuarioResponse(BaseModel):
    id: Optional[ObjectId] = Field(alias="_id")
    username: str
    nome: str
    
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)


class UsuarioDBModel(UsuarioResponse):
    def model_dump(
        self,
        *,
        mode="python",
        include=None,
        exclude=None,
        context=None,
        by_alias=None,
        exclude_unset=False,
        exclude_defaults=False,
        exclude_none=False,
        exclude_computed_fields=False,
        round_trip=False,
        warnings=True,
        fallback=None,
        serialize_as_any=False
    ):
        data = super().model_dump(
            mode=mode,
            include=include,
            exclude=exclude,
            context=context,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            exclude_computed_fields=exclude_computed_fields,
            round_trip=round_trip,
            warnings=warnings,
            fallback=fallback,
            serialize_as_any=serialize_as_any,
        )
        
        if self.id:
            data["_id"] = str(data["_id"])
        
        return data
