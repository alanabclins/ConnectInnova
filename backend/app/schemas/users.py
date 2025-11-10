from typing import Optional
from uuid import UUID
import re
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    """
    Shared User properties. Visible by anyone.
    """

    name: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    picture: Optional[str] = None

    @field_validator('name', 'first_name', 'last_name')
    def name_validator(cls, v):
        if not v:
            return v
        if not re.match(r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$", v):
            raise ValueError("O nome contém caracteres inválidos")
        return v

class PrivateUserBase(UserBase):
    """
    Shared User properties. Visible only by admins and self.
    """

    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    provider: Optional[str] = None


class UserUpdate(UserBase):
    """
    User properties to receive via API on update.
    """

    password: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    provider: Optional[str] = None


class User(PrivateUserBase):
    """
    User properties returned by API. Contains private
    user information such as email, is_active, auth provider.

    Should only be returned to admins or self.
    """

    id: PydanticObjectId = Field()
    uuid: UUID
    hashed_password: Optional[str] = None
    updated_at: Optional[str] = None
