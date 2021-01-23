from typing import List, Optional
from pydantic import Field
from models.base import CustomBaseModel


class NewIntegration(CustomBaseModel):
    integration: str = None
    type: str = None
    key: str = None
    version: str = None
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
    tags: Optional[List[str]] = None
    timestamp: float = None

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "integration": "Slack Deployments Prod",
                "type": "Slack",
                "key": "my-slack-api-key",
                "enabled": True,
                "created_timestamp": 1610146671,
                "modified_timestamp": 1610146671,
                "created_by": "admin@example.com",
                "modified_by": "admin@example.com",
                "tags": {
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
                "custom": {
                    "module": "foo",
                    "color": "green"
                }
            }
        }
