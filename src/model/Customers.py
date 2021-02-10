import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, INTEGER, DateTime, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from . import Base


class CustomersSchema(Base):
    __tablename__ = "costumers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True)
    name = Column(String)
    street_address = Column(String)
    address_number = Column(String)
    city = Column(String)
    state = Column(String)
    zip_code = Column(INTEGER)
    geolocation = Column(String)
    associated_route = Column(String, default="Outros")
    creation_date = Column(DateTime, default=datetime.datetime.now)
    last_update = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    class Config:
        schema_extra = {
            "example": {
                "name": "Costumer_1",
                "geolocation": "(40.721959482, -73.878993913)"
            }
        }
