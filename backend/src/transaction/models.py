from sqlalchemy import Column, String, Float ,Integer , DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID 
from datetime import datetime, timezone 
import uuid 
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_points = Column(Float, default=0.0)
    transaction_count = Column(Integer,default=0)
    last_transaction_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    points = Column(Float, nullable=False)
    idempotency_key = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    


    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_idempotency_key"),
    )