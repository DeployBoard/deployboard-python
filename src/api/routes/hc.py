import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/hc", tags=["HealthCheck"], responses={404: {"description": "Not found"}}
)


@router.get("/")
async def hc():
    """
    Returns a 200 for the load balancer health check.
    """
    return 200
