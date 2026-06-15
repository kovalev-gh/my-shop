# app/domains/users/schemas.py

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None

class UserUpdatePartial(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    is_admin: bool | None = None


class UserRead(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )