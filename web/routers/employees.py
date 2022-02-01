from typing import List

from fastapi import APIRouter
from fastapi.params import Depends

from db.models import GetEmployee, Employee
from db.repositories import EmployeesRepository
from utils import config
from ..dependencies import get_db

router = APIRouter()


@router.get("/employees", response_description="List employees", response_model=List[Employee])
async def list_employees(
        get_employee: GetEmployee = Depends(),  # type: ignore
        offset: int = 0,
        limit: int = config.GET_ENTITIES_DEFAULT_LIMIT,
        db=Depends(get_db)
):
    results = await EmployeesRepository(db).get_many(
        get_model=get_employee, offset=offset, limit=limit
    )
    return results
