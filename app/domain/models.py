from typing import Optional
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class UserUpdate(BaseModel):
    new_name: str

class ProductCreate(BaseModel):
    name: str
    user_id: Optional[int] = None

class ProductUpdate(BaseModel):
    new_name: str
    new_user_id: Optional[int] = None

class ProductSchema(BaseModel):
    id: int
    name: str
    user_id: Optional[int] = None

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    id: int
    name: str
    products: list[ProductSchema] = []

    class Config:
        orm_mode = True
