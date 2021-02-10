from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import datetime
from uuid import uuid4
from . import Base


class SellerSchema(Base):
    __tablename__ = "sellers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True)
    name = Column(String)
    email = Column(String, unique=True)
    creation_date = Column(DateTime, default=datetime.datetime.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    class Config:
        schema_extra = {
            "example": {
                "name": "Seller_1",
                "email": "seller_1@email.com"
            }
        }