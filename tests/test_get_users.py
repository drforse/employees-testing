import asyncio
import datetime
import json

import pytest
from httpx import AsyncClient

from db.core import client as motor_client
from db.models import Employee
from utils import config
from web import app
from web.dependencies import get_db


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def employees_models() -> list[Employee]:
    with open("tests/data/employees.json") as f:
        return [Employee(**e) for e in json.load(f)]


@pytest.fixture(scope="session")
def employees(employees_models) -> list[dict]:
    result = []
    for e in employees_models:
        e.join_date = e.join_date.astimezone(datetime.timezone.utc)
        result.append(json.loads(e.json(by_alias=True)))
    return result


@pytest.fixture(scope="session")
def employees_insert(employees_models) -> list[dict]:
    return [e.dict(by_alias=True) for e in employees_models]


@pytest.fixture(scope="session", autouse=True)
async def db(employees_insert):
    motor_client.get_io_loop = asyncio.get_running_loop
    db = motor_client[config.TEST_MONGO_DB]
    col = db.get_collection("employees")
    await col.insert_many(employees_insert)
    yield db
    await motor_client.drop_database(config.TEST_MONGO_DB)


@pytest.fixture
def fastapi_app(db):
    fastapi_app = app()
    fastapi_app.dependency_overrides[get_db] = lambda: db
    return fastapi_app


@pytest.mark.anyio
async def test_all_returned(fastapi_app, employees):
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/employees?limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == employees[:1000]


@pytest.mark.anyio
async def test_limit(fastapi_app, employees):
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/employees?limit=20")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == employees[:20]


@pytest.mark.anyio
async def test_offset_and_limit(fastapi_app, employees):
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get("/employees?offset=20&limit=50")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == employees[20:70]


@pytest.mark.anyio
async def test_filter_name(fastapi_app, employees):
    name = employees[0]["name"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?name={name}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["name"] == name, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_email(fastapi_app, employees):
    email = employees[1]["email"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?email={email}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["email"] == email, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_age(fastapi_app, employees):
    age = employees[2]["age"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?age={age}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["age"] == age, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_company(fastapi_app, employees):
    company = employees[2]["company"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?company={company}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["company"] == company, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_join_date(fastapi_app, employees):
    join_date = employees[3]["join_date"]
    print(f'{join_date=}')
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?join_date={join_date}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["join_date"] == join_date, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_job_title(fastapi_app, employees):
    job_title = employees[4]["job_title"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?job_title={job_title}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["job_title"] == job_title, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_gender(fastapi_app, employees):
    gender = "male"
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?gender={gender}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["gender"] == gender, employees[:1000])
    )


@pytest.mark.anyio
async def test_filter_salary(fastapi_app, employees):
    salary = employees[6]["salary"]
    async with AsyncClient(app=fastapi_app, base_url="http://localhost:8000") as ac:
        response = await ac.get(f"/employees?salary={salary}&limit=1000")
    assert response.status_code == 200
    assert [json.loads(Employee(**e).json(by_alias=True)) for e in response.json()] == list(
        filter(lambda e: e["salary"] == salary, employees[:1000])
    )
