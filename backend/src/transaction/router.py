from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from database import get_db 
from src.transaction.schemas import UserCreate, UserResponse, TransactionCreate, TransactionResponse, UserSummaryResponse, RankingResponse 
from src.transaction import controller

router = APIRouter(prefix="/api", tags=["Transactions"])

#POST api/user
@router.post("/user", response_model=  UserResponse)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await controller.create_user(data,db)


#POST api/transaction
@router.post("/transaction", response_model= TransactionResponse, status_code=201)
async def create_transaction(data: TransactionCreate, db: AsyncSession = Depends(get_db)):
    return await controller.create_transaction(data,db)


#GET /api/summary/{user_id}
@router.get("/summary/{user_id}", response_model=UserSummaryResponse)
async def get_summary(user_id: str, db: AsyncSession = Depends(get_db)):
    return await controller.get_user_summary(user_id, db)


#GET /api/ranking
@router.get("/ranking", response_model=RankingResponse)
async def get_ranking(db: AsyncSession = Depends(get_db)):
    return await controller.get_ranking(db)
