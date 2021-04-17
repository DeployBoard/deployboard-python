from pydantic import BaseModel, Field


class CustomBaseModel(BaseModel):
    schema_version: float = Field(1.0, const=True)

    class Config:
        schema_extra = {"example": {"schema": 1.0}}
