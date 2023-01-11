import uvicorn
from fastapi import FastAPI

from core.config import WEB_PORT, WEB_HOST
from db.base import database
from endpoints import users, auth, posts, rate

app = FastAPI(title="Webtronics FastAPI application")
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(posts.router, prefix="/posts", tags=["posts"])
app.include_router(rate.router, prefix="/rating", tags=["rating"])


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


if __name__ == "__main__":
    uvicorn.run("main:app", port=int(WEB_PORT), host=WEB_HOST, reload=True)
