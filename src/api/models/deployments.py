from typing import Optional
from models.base import CustomBaseModel


class DeploymentRequest(CustomBaseModel):
    application: str
    service: str
    environment: str
    status: str
    version: str
    custom: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "application": "SampleApp",
                "service": "SampleService",
                "environment": "Prod",
                "status": "Deploying",
                "version": "v1.0.2",
                "custom": {
                    "module": "example-module",
                    "user": "JohnDoe"
                }
            }
        }
