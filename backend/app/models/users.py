from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID, uuid4

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """
    User Model - SCRUM-47

    Collection managed by Beanie ODM.

    Fields:

    - uuid: Unique user identifier (UUID)
    - email: Unique email address (required)
    - name: Full name (optional)
    - first_name: First name (optional)
    - last_name: Last name (optional)
    - hashed_password: Password hash (optional)
    - provider: Authentication provider (optional)
    - picture: URL to profile picture (optional)
    - is_active: User active status (default True)
    - is_superuser: Superuser status (default False)
    - updated_at: Last update timestamp (optional)
    """

    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)] = Field(
        default_factory=uuid4
    )
    email: Annotated[EmailStr, Indexed(unique=True)]
    name: Annotated[str, Field(min_length=1)]
    first_name: str | None = None
    last_name: str | None = None
    hashed_password: str | None = None
    provider: str | None = None
    picture: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    updated_at: datetime | None = None
    reset_token: Optional[str] = None
    reset_token_expires: Optional[datetime] = None