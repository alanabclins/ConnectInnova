from typing import Optional
from uuid import UUID

from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """
    Shared User properties. Visible by anyone.
    """

    name: str = ""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    picture: Optional[str] = None


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
