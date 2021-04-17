from typing import List, Optional

from models.base import CustomBaseModel
from pydantic import BaseModel, Field


class ServiceEnvironment(BaseModel):
    status: str = None
    version: str = None
    timestamp: int = None
    custom: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "status": "Deployed",
                "version": "1.2.1",
                "timestamp": 1608633640,
                "custom": {"module": "foo", "color": "green"},
            }
        }


class NewService(CustomBaseModel):
    service: str
    application: str

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "service": "API",
                "application": "DeployBoard",
                "tags": [],
                "environments": {},
            }
        }


class Service(NewService):
    account: str
    tags: Optional[List[str]] = []
    environments: Optional[dict] = {}

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "account": "DeployBoard",
                "service": "API",
                "application": "DeployBoard",
                "tags": ["backend", "python", "fastapi"],
                "environments": {
                    "Dev": {
                        "status": "Deployed",
                        "version": "1.2.1",
                        "timestamp": 1608633640,
                        "custom": {"module": "foo", "color": "green"},
                    },
                    "Prod": {
                        "status": "Deployed",
                        "version": "1.2.0",
                        "timestamp": 1608623640,
                        "custom": {"module": "foo", "color": "green"},
                    },
                },
            }
        }


class ServiceResponse(Service):
    id: str = Field(..., alias="_id")

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "_id": "5ff29f4ade185a01cd6ae45d",
                "schema_version": 1.0,
                "account": "DeployBoard",
                "service": "API",
                "application": "DeployBoard",
                "tags": ["backend", "python", "fastapi"],
                "environments": {
                    "Dev": {
                        "status": "Deployed",
                        "version": "1.2.1",
                        "timestamp": 1608633640,
                        "custom": {"module": "foo", "color": "green"},
                    },
                    "Prod": {
                        "status": "Deployed",
                        "version": "1.2.0",
                        "timestamp": 1608623640,
                        "custom": {"module": "foo", "color": "green"},
                    },
                },
            }
        }
