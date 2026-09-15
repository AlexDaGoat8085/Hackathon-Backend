import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Fallback to local SQLite if config DB_URL is missing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./hackathon_local.db")

try:
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        future=True,
        pool_size=20,
        max_overflow=10
    )
except Exception as e:
    print(f"Failed to initialize async engine: {e}")

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()

async def get_db_session() -> AsyncSession:
    """
    Dependency generator for FastAPI dependency injection.
    Ensures safe rollback on transaction failure.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as db_ex:
            await session.rollback()
            raise db_ex
        finally:
            await session.close()
