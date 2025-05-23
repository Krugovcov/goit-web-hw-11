import  contextlib

from sqlalchemy.ext.asyncio import  AsyncSession, AsyncEngine,  create_async_engine, async_sessionmaker


from src.conf.conf import config

class DatabaseSessionManager:
    def __init__(self, url:str):
        self._engine: AsyncEngine |None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False, autocommit=False, bind=self._engine)
        
    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not installed")
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
            raise 
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(config.DB_URL)

async def get_db():
    async with sessionmanager.session() as session:
        yield session
