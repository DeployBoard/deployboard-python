from typing import List, Optional
from pydantic import Field
from models.base import CustomBaseModel


class NewLog(CustomBaseModel):
    service: str
    application: str
    environment: str
    status: str
    version: str
    custom: Optional[dict] = None

    class Config:
        schema_extra = {
            "service": "Api",
            "application": "Sample",
            "environment": "Dev",
            "status": "Deploying",
            "version": "1.3.0",
            "custom": {
                "module": "foo",
                "color": "green"
            }
        }


class Log(NewLog):
    account: str
    timestamp: float
    hash: str
    hash_chain: str
    tags: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "account": "Example",
                "service": "Api",
                "application": "Sample",
                "environment": "Dev",
                "status": "Deploying",
                "version": "1.3.0",
                "timestamp": 1610146671,
                "hash": "a7cd6c222ea5fc1463c0ca3f70b93035196c8c4f34d89181ff5086bd7b58bfff",
                "hash_chain": "6a9ec5bf3b15354e1cb8599e2262a9ff8d808d793987399bb9bd41c949cd661a",
                "custom": {
                    "module": "foo",
                    "color": "green"
                }
            }
        }


class LogResponse(Log):
    id: str = Field(..., alias='_id')

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "5ff89d1f0ab150bbf4cccbe4",
                "schema_version": 1.0,
                "account": "Example",
                "service": "Api",
                "application": "Sample",
                "environment": "Dev",
                "status": "Deploying",
                "version": "1.3.0",
                "timestamp": 1610146671,
                "hash": "a7cd6c222ea5fc1463c0ca3f70b93035196c8c4f34d89181ff5086bd7b58bfff",
                "hash_chain": "6a9ec5bf3b15354e1cb8599e2262a9ff8d808d793987399bb9bd41c949cd661a",
                "custom": {
                    "module": "foo",
                    "color": "green"
                }
            }
        }
