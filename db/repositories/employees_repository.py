from .base import BaseRepository
from ..models import Employee, GetEmployee


class EmployeesRepository(BaseRepository[Employee, GetEmployee]):
    __collection_name__ = "employees"
