from fastapi import FastAPI
from database import engine, Base
from fastapi.middleware.cors import CORSMiddleware 
from contextlib import asynccontextmanager

from src.transaction import models
from src.transaction.router import router 


@asynccontextmanager 
async def lifespan(app: FastAPI):

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 


app = FastAPI(title="Transaction leaderboard API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Transaction Leaderboard API is running"}