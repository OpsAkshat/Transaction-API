from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func 
from sqlalchemy.exc import IntegrityError 
from fastapi import HTTPException 
from datetime import datetime , timezone 
import asyncio 
import uuid
from src.transaction.models import User , Transaction 
from src.transaction.schemas import UserCreate, TransactionCreate 



_user_locks: dict[str, asyncio.Lock] = {}

def get_user_lock(user_id: str) -> asyncio.Lock:
    if user_id not in _user_locks:
        _user_locks[user_id] = asyncio.Lock()
    return _user_locks[user_id]



async def create_user(data: UserCreate, db: AsyncSession):

    exist = await db.execute(select(User).where(User.name == data.name))
    if exist.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User with this name already exists")


    user = User(id=str(uuid.uuid4()),name=data.name)

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_transaction(data: TransactionCreate, db: AsyncSession):
    
    user = await db.get(User , data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.points > 10000:
        raise HTTPException(status_code = 400, detail="Points cannot exceed 10,000 per transaction")


    async with get_user_lock(data.user_id):
        try:
            txn = Transaction(
                user_id=data.user_id,
                points=data.points,
                idempotency_key=str(uuid.uuid4())
            )
            db.add(txn)

            user.total_points += data.points
            user.transaction_count +=1 
            user.last_transaction_at = datetime.now(timezone.utc)

            await db.commit()
            await db.refresh(txn)
            return txn 

        except IntegrityError:
            await db.rollback()
            raise HTTPException(status_code=409, detail="Duplicate transaction")    


async def get_user_summary(user_id: str, db: AsyncSession):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail= "User not found")

    result = await db.execute(
        select(Transaction).where(Transaction.user_id == user_id ).order_by(Transaction.created_at.desc())
    )   
    transactions = result.scalars().all()

    return{
        "user_id": user.id,
        "name": user.name,
        "total_points": user.total_points,
        "transaction_count": user.transaction_count, 
        "last_transaction_at": user.last_transaction_at,
        "transactions": transactions
    }

async def get_ranking(db: AsyncSession):
    result = await db.execute(select(User))
    users = result.scalars().all()

    if not users: 
        return {"total_users": 0 , "rankings": []}

    max_points = max(u.total_points for u in users) or 1
    max_count = max(u.transaction_count for u in users) or 1

    now = datetime.now(timezone.utc)
    ranked = []

    for user in users:
        
        # factor 1 (wieght: 60%)
        points_score = (user.total_points / max_points) * 60
        
        # factor 2 (weight: 25%)
        consistency_score = (user.transaction_count / max_count) * 25
        
        #factor 3 (weight: 15%)
        if user.last_transaction_at:
            last = user.last_transaction_at
            if last.tzinfo is None: 
                last = last.replace(tzinfo=timezone.utc)

            days_since = (now - last).days
            recency_score = max(0, 15 - days_since)
        else: 
            recency_score = 0 

        ranking_score = round(points_score + consistency_score + recency_score, 2)

        ranked.append({
            "user_id": user.id,
            "name": user.name,
            "total_points": user.total_points,
            "transaction_count": user.transaction_count, 
            "last_transaction_at": user.last_transaction_at,
            "ranking_Score": ranking_score
        }) 

    ranked.sort(key=lambda x: x["ranking_Score"], reverse= True)
    for i, entry in enumerate(ranked):
        entry["rank"] = i + 1
    return {"total_users": len(ranked), "rankings": ranked}

    