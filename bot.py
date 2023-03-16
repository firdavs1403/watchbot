import asyncio
import os

from aiogram.fsm.storage.memory import MemoryStorage
from config import config
import logging
from aiogram import Bot, Dispatcher
import handlers
from sqlalchemy.ext.asyncio import create_async_engine
from db import get_session_maker, proceed_schemas, Base

logging.basicConfig(level=logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    dp.include_router(handlers.router)

    engine = create_async_engine(f"postgresql+asyncpg://{os.getenv('name')}:{os.getenv('password')}@localhost:8080/{os.getenv('db_name')}")
    session_maker = get_session_maker(engine)
    await proceed_schemas(engine, Base.metadata)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types(), session_maker=session_maker)


if __name__ == '__main__':
    asyncio.run(main())
