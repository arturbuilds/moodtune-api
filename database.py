from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
load_dotenv()

database_url = 'sqlite+aiosqlite:///./moodtune.db'
engine = create_async_engine(database_url)

AsyncSessionLocal = async_sessionmaker(bind=engine)
Base = declarative_base()

async def get_async_db():
    async with AsyncSessionLocal() as db:
        yield db