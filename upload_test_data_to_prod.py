import asyncio
import json

from db.core import client
from db.models import Employee
from utils import config


async def main():
    with open("resources/employees.json") as f:
        employees = [Employee(**e).dict(by_alias=True) for e in json.load(f)]

    client.get_io_loop = asyncio.get_running_loop
    db = client[config.MONGO_DB]
    col = db.get_collection("employees")
    await col.insert_many(employees)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
