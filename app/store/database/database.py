from typing import Optional, TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.store.database import db

if TYPE_CHECKING:
    from app.web.app import Application

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[declarative_base] = None
        self.session: Optional[AsyncSession] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(DATABASE_URL, echo=True, future=True)
        self.session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self.app.logger.info("Database connected")

    async def disconnect(self, *_: list, **__: dict) -> None:
        self.app.logger.info("Database disconnected")
