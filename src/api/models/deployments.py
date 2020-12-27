from typing import Optional
from pydantic import Field
from models.base import CustomBaseModel


class DeploymentRequest(CustomBaseModel):
    app: str = None
    service: str = None
    env: str = None
    status: str = None
    version: str = None
    custom: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "app": "SampleApp",
                "service": "SampleService",
                "env": "Prod",
                "status": "Deploying",
                "version": "v1.0.2",
                "custom": {
                    "module": "example-module",
                    "user": "JohnDoe"
                }
            }
        }


class Deployment(DeploymentRequest):
    timestamp: int = None
    account: str = None

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "account": "Acme",
                "app": "SampleApp",
                "service": "SampleService",
                "env": "Prod",
                "status": "Deploying",
                "version": "v1.0.2",
                "timestamp": 123456789,
                "custom": {
                    "module": "example-module",
                    "user": "JohnDoe"
                }
            }
        }


class DeploymentResponse(Deployment):
    id: str = Field(..., alias='_id')

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe7d7aedc0bf29191dbd0e9",
                "schema_version": 1.0,
                "account": "Acme",
                "app": "SampleApp",
                "service": "SampleService",
                "env": "Prod",
                "status": "Deploying",
                "version": "v1.0.2",
                "timestamp": 123456789,
                "custom": {
                    "module": "example-module",
                    "user": "JohnDoe"
                }
            }
        }
