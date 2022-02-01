import abc
import datetime

from bson import ObjectId
from pydantic import BaseModel as PydanticModel


class BaseModel(abc.ABC, PydanticModel):

    class Config:
        use_enum_values = True
        allow_population_by_field_name = False
        orm_mode = True
        validate_assignment = True
        json_encoders = {
            datetime.datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S"),
            ObjectId: str
        }
