from typing import List
from pydantic import BaseModel
from models.base import CustomBaseModel


class UpdateEnvironment(CustomBaseModel):
    environments: List[str]

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1,
                "environments": ["Production", "Test", "Dev"]
            }
        }


class EnvironmentResponse(BaseModel):
    environments: List[str]

    class Config:
        schema_extra = {
            "example": {
                "environments": ["Production", "Test", "Dev"]
            }
        }
