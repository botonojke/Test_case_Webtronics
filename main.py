import uvicorn
from fastapi import FastAPI

from core.config import WEB_PORT, WEB_HOST
from db.base import database

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=int(WEB_PORT), host=WEB_HOST, reload=True)
