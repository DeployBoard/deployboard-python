from typing import Optional
from pydantic import EmailStr, Field, BaseModel
from models.base import CustomBaseModel


class User(CustomBaseModel):
    account: str = None
    email: EmailStr = None
    role: str = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar: Optional[str] = None
    theme: Optional[str] = None
    enabled: bool = True

    class Config:
        schema_extra = {
            "example": {
                "schema_version": 1.0,
                "account": "example",
                "email": "jdoe@example.com",
                "role": "Editor",
                "first_name": "John",
                "last_name": "Doe",
                "enabled": True
            }
        }


class UserResponse(User):
    id: str = Field(..., alias='_id')
    created_timestamp: float = None
    modified_timestamp: float = None
    modified_by: str = None
    password_expires: float = None

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe51081e178d1bda551cc2a",
                "schema_version": 1.0,
                "account": "example",
                "email": "jdoe@example.com",
                "role": "Editor",
                "first_name": "John",
                "last_name": "Doe",
                "enabled": True,
                "created_timestamp": 1610053395,
                "modified_timestamp": 1610053395,
                "modified_by": "admin@example.com",
                "password_expires": 1610053395
            }
        }


class UserInDB(User):
    hashed_password: str = None
    salt: str = None
    password_expires: float = None

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe51081e178d1bda551cc2a",
                "schema_version": 1.0,
                "account": "example",
                "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
                "salt": "cgGmUECGkYRiKEcnuhyr",
                "email": "jdoe@example.com",
                "role": "Editor",
                "first_name": "John",
                "last_name": "Doe",
                "enabled": True,
                "password_expires": 1610053395
            }
        }


class CreateUser(CustomBaseModel):
    email: EmailStr
    role: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    enabled: bool = True
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "jdoe2@example.com",
                "role": "Editor",
                "first_name": "John",
                "last_name": "Doe2",
                "enabled": True,
                "password": "secret"
            }
        }


class UpdateUserAsAdmin(CustomBaseModel):
    _id: str = None
    email: Optional[EmailStr]
    role: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    enabled: Optional[bool]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "_id": "5fe14013fc83e4c8f18ff9b5",
                "email": "jdoe@example.com",
                "role": "Viewer",
                "first_name": "John",
                "last_name": "Doe",
                "enabled": False,
                "password": "supersecretpassword"
            }
        }


class UpdateUserAsSelf(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    theme: Optional[str]
    avatar: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "theme": "dark",
                "avatar": "https://avatars.com/my_avatar.png",
                "password": "supersecretpassword"
            }
        }
