from typing import Union
from fastapi import FastAPI
from .routers import datapoint

app = FastAPI()
app.include_router(datapoint.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
