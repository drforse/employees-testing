from datetime import datetime, timezone
from typing import Optional

from pydantic import Field

from utils.pydantic_fields import PyObjectId
from .base import BaseModel
from .enums import GenderEnum


class Employee(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    email: str
    age: int
    company: str
    join_date: datetime  # TODO: store offset alongside
    job_title: str
    gender: GenderEnum
    salary: int


class GetEmployee(BaseModel):
    name: Optional[str]
    email: Optional[str]
    age: Optional[int]
    company: Optional[str]
    join_date: Optional[datetime]
    job_title: Optional[str]
    gender: Optional[GenderEnum]
    salary: Optional[int]
