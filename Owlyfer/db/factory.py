from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker


engine = create_async_engine("sqlite+aiosqlite:///sqlalchemy.db", echo=True)

async_session_factory = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
