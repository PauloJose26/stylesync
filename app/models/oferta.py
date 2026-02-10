from pydantic import BaseModel, ConfigDict
from datetime import date


class Oferta(BaseModel):
    data_oferta: date
    produto_id: str
    quantidade: int
    valor_total: float

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

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
        
        if self.data_oferta:
            data["data_oferta"] = self.data_oferta.strftime("%Y-%m-%d")
        
        return data
