from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, Binary
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import datetime
from uuid import uuid4
from . import Base


class UserSchema(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex, unique=True)
    fullname = Column(String)
    email = Column(String)
    password = Column(Binary)
    role = Column(String, default='user')
    creation_date = Column(DateTime, default=datetime.datetime.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    class Config:
        schema_extra = {
            "example": {
                "fullname": "user_1",
                "email": "user_1@email.com",
                "password": "password"
            }
        }


class UserLoginSchema(Base):
    __tablename__ = "users_login"
    session_id = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password = Column(Binary)
    user_role = Column(String, default='user')
    login_date = Column(DateTime, default=datetime.datetime.now())

    class Config:
        schema_extra = {
            "example": {
                "email": "user_1@x.com",
                "password": "password"
            }
        }
