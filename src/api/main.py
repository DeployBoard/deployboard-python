import logging
from fastapi import FastAPI, Request
from routes import token, deploy, services, logs, users, me, apikeys, environments
import time


logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="DeployBoard",
    description="Deployment Tracking",
    version="0.1.0"
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(token.router)
app.include_router(deploy.router)
app.include_router(services.router)
app.include_router(logs.router)
app.include_router(users.router)
app.include_router(me.router)
app.include_router(apikeys.router)
app.include_router(environments.router)
