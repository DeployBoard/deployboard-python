from typing import Optional
from pydantic import EmailStr, Field
from models.base import CustomBaseModel


class ApiKey(CustomBaseModel):
    account: str = None
    name: str = None
    role: str = None
    enabled: bool = True
    created_by: EmailStr = None
    created_timestamp: float = None
    modified_by: EmailStr = None
    modified_timestamp: float = None

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1,
                "account": "Example",
                "name": "test-api-key",
                "role": "Editor",
                "enabled": True,
                "created_by": "jdoe@example.com",
                "created_timestamp": 1610053395,
                "modified_by": "admin@example.com",
                "modified_timestamp": 1610921529
            }
        }


class ApiKeyResponse(ApiKey):
    id: str = Field(..., alias='_id')

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe51081e178d1bda551cc2a",
                "schema_version": 1,
                "account": "Example",
                "name": "test-api-key",
                "role": "Editor",
                "enabled": True,
                "created_by": "jdoe@example.com",
                "created_timestamp": 1610053395,
                "modified_by": "admin@example.com",
                "modified_timestamp": 1610921529
            }
        }


class CreateApiKey(CustomBaseModel):
    name: str = None
    role: str = None
    enabled: Optional[bool] = Field(True, const=True)

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "name": "test-api-key",
                "role": "Editor"
            }
        }


class UpdateApiKey(CustomBaseModel):
    _id: str = None
    name: Optional[EmailStr]
    role: Optional[str]
    enabled: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe14013fc83e4c8f18ff9b5",
                "name": "test-api-key",
                "role": "Editor",
                "enabled": False
            }
        }
