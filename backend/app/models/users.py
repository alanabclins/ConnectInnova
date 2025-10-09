from typing import Annotated
from uuid import UUID, uuid4
from datetime import datetime

from beanie import Document, Indexed
from pydantic import EmailStr, Field


class User(Document):
    """
    User Model - SCRUM-47
    Collection managed by Beanie ODM
    
    Required fields:
    - user_id: Automatic MongoDB ObjectId (_id)
    - name: Full user name
    - email: Unique email
    - password_hash: Password hash
    - created_at: Creation timestamp
    """
    # Required field: user_id (additional uuid for compatibility)
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)]
    
    # Required field: name
    name: str
    
    # Required field: email (unique)
    email: Annotated[EmailStr, Indexed(unique=True)]
    
    # Required field: password_hash
    password_hash: str
    
    # Required field: created_at
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Optional fields (compatibility with existing system)
    first_name: str | None = None
    last_name: str | None = None
    hashed_password: str | None = None  # Kept for backward compatibility
    provider: str | None = None
    picture: str | None = None
    is_active: bool = True
    is_superuser: bool = False
    updated_at: datetime | None = None
