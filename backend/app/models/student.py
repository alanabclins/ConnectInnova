from typing import Annotated, Optional
from uuid import UUID, uuid4
from beanie import Document, Indexed
from pydantic import Field


class Student(Document):
    uuid: Annotated[UUID, Field(default_factory=uuid4), Indexed(unique=True)]
    name: str
    student_description: str
    curriculum: Optional[str] = None
    academic_informations: str
    skills_experiencies: str

    class Settings:
        name = "Student"  # nome da coleção no MongoDB
