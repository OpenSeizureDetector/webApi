import asyncio

import uvloop
from fastapi import FastAPI
from .routers import datapoint

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
app = FastAPI()
app.include_router(datapoint.router)


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


@app.head("/healthcheck")
@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
