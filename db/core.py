import motor.motor_asyncio

from utils import config


client = motor.motor_asyncio.AsyncIOMotorClient(config.MOTOR_URI)
