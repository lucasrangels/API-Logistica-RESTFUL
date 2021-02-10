from sqlalchemy import Column, String, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSON
import datetime
from uuid import uuid4
from . import Base


class RouteSchema(Base):
    __tablename__ = "routes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=lambda: uuid4().hex, unique=True)
    name = Column(String, unique=True, nullable=False)
    bounds = Column(JSON, nullable=False, default=dict, server_default='{}')
    seller_id = Column(UUID, ForeignKey('sellers.id'),  unique=True, nullable=True)
    creation_date = Column(DateTime, default=datetime.datetime.now())
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())
    seller = relationship("SellerSchema")

    class Config:
        schema_extra = {
            "example": {
                "name": "Rota 1",
                "bounds": "Poligono 2D",
                "seller_name": "Ronaldo"
            }
        }
