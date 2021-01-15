from typing import Optional, List
from pydantic import BaseModel


class Service(BaseModel):
    tags: Optional[List[str]] = None
    versions: Optional[List[ServiceVersion]] = None

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "schema": 1.0,
                "service": "API",
                "application": "DeployBoard",
                "account": "DeployBoard",
                "tags": ["backend", "python", "fastapi"],
                "versions": [
                    {
                        "environment": "Dev",
                        "status": "Deployed",
                        "version": "1.2.1",
                        "timestamp": "1608633640",
                        "custom": {
                            "module": "foo",
                            "color": "green"
                        }
                    },
                    {
                        "environment": "Prod",
                        "status": "Deployed",
                        "version": "1.2.0",
                        "timestamp": "1608623640",
                        "custom": {
                            "module": "foo",
                            "color": "green"
                        }
                    }
                ]
            }
        }
