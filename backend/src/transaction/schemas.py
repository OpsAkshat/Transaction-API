from operator import imatmul
import uuid
from pydantic import BaseModel, Field, model_validator
from typing import Optional, List
from datetime import datetime 
from uuid import UUID


# REQUEST 

class UserCreate(BaseModel):
    name: str

    @model_validator(mode="after")
    def check_fields(self):
        if not self.name.strip():
            raise ValueError("name cannot be blank")
        return self



class TransactionCreate(BaseModel):
    user_id : str
    points: float = Field(..., gt= 0, description= "Points must be greater than 0")
    

    @model_validator(mode="after")
    def check_fields(self):
        if not self.user_id.strip():
            raise ValueError("user_id cannot be blank")
        if self.points <= 0:
            raise ValueError("points must be greater than 0")
        return self


#RESPONSE 

class TransactionResponse(BaseModel):
    id: UUID
    user_id : str
    points: float 
    idempotency_key: str
    created_at: datetime 

    class Config:
        from_attributes = True 



class UserResponse(BaseModel):
    id: str
    name: str
    total_points: float
    transaction_count: int
    created_at: datetime

    class Config:
        from_attributes = True



class UserSummaryResponse(BaseModel): 
    user_id: str 
    name: str 
    total_points: float 
    transaction_count: int
    last_transaction_at: Optional[datetime]
    transactions: List[TransactionResponse] 

    class Config:
        from_attributes = True

class RankedUser(BaseModel):
    rank : int
    user_id: str
    name: str
    total_points: float 
    transaction_count: int
    last_transaction_at: Optional[datetime]
    ranking_Score: float 

    class Config:
        from_attributes = True 


class RankingResponse(BaseModel):
    total_users: int
    rankings: List[RankedUser]



    