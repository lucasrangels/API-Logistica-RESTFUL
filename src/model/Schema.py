from pydantic import BaseModel, Json


class UserSchema(BaseModel):
    fullname: str = None
    email: str = None
    password: str = None

    class Config:
        orm_mode = True


class UserLoginSchema(BaseModel):
    email: str
    password: str = None

    class Config:
        orm_mode = True


class RouteSchema(BaseModel):
    name: str = None
    bounds: str = None

    class Config:
        orm_mode = True


class SellerSchema(BaseModel):
    name: str = None
    email: str = None

    class Config:
        orm_mode = True


class CostumerSchema(BaseModel):
    name: str = None
    street_address: str = None
    address_number: str = None
    city: str = None
    state: str = None
    zip_code: int = None

    class Config:
        orm_mode = True


class NameCostumerSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class AssignSchema(BaseModel):
    route_name: str
    seller_email: str

    class Config:
        orm_mode = True
