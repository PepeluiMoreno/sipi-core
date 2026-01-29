
# db/sessions/manager.py

from typing import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, AsyncAdaptedQueuePool
import os


class DatabaseConfig:
    """Configuración compartida para conexiones de base de datos"""
    
    @staticmethod
    def get_database_url(async_mode: bool = False) -> str:
        """Obtiene la URL de la base de datos desde variables de entorno"""
        database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            user = os.getenv("POSTGRES_USER", "sipi")
            password = os.getenv("POSTGRES_PASSWORD", "sipi")
            host = os.getenv("POSTGRES_SERVICE_NAME", "localhost")
            port = os.getenv("POSTGRES_PORT", "5432")
            db = os.getenv("POSTGRES_DB", "sipi")
            database_url = f"postgresql://{user}:{password}@{host}:{port}/{db}"
        
        # Normalizar a formato síncrono primero
        database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
        database_url = database_url.replace("postgresql+psycopg2://", "postgresql://")
        
        if async_mode:
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
        
        return database_url
    
    @staticmethod
    def get_schema() -> str:
        """Obtiene el schema principal desde variables de entorno"""
        return os.getenv("DATABASE_SCHEMA", "app")
    
    @staticmethod
    def get_defined_schemas() -> list[str]:
        """Obtiene la lista de schemas definidos"""
        from db.metadata import APP_SCHEMA, GIS_SCHEMA
        schemas = os.getenv("DEFINED_SCHEMAS", f"{APP_SCHEMA},{GIS_SCHEMA}")
        return schemas.split(",")


class SyncDatabaseManager:
    """
    Manager síncrono para conexiones a base de datos.
    Usado por Alembic y operaciones síncronas.
    """
    
    def __init__(self, database_url: str = None, echo: bool = False, **pool_kwargs):
        self.database_url = database_url or DatabaseConfig.get_database_url(async_mode=False)
        self.schema = DatabaseConfig.get_schema()
        self.defined_schemas = DatabaseConfig.get_defined_schemas()
        
        # Conectar con search_path configurado
        connect_args = {
            "options": f"-c search_path={','.join(self.defined_schemas)},public"
        }
        
        self.engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            echo=echo,
            connect_args=connect_args,
            **pool_kwargs
        )
        
        self.session_maker = sessionmaker(
            self.engine,
            class_=Session,
            expire_on_commit=False,
        )
    
    def close(self):
        """Cierra el engine"""
        self.engine.dispose()
    
    @contextmanager
    def session(self) -> Generator[Session, None, None]:
        """Context manager para sesiones de base de datos"""
        session = self.session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def get_session(self) -> Generator[Session, None, None]:
        """Generator para dependencias (estilo FastAPI)"""
        session = self.session_maker()
        try:
            yield session
        finally:
            session.close()
    
    def init_database(self):
        """Inicializa la base de datos: extensiones, schemas, etc."""
        with self.session() as session:
            # Verificar conexión
            session.execute(text("SELECT 1"))
            
            # Extensiones PostGIS
            session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
            
            # Crear schemas definidos
            for schema in self.defined_schemas:
                session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            
            # Configurar search_path
            search_path = ','.join(self.defined_schemas) + ',public'
            session.execute(text(f"SET search_path TO {search_path}"))
            
            session.commit()
    
    def execute(self, sql: str, params: dict = None):
        """Ejecuta SQL directamente"""
        with self.session() as session:
            result = session.execute(text(sql), params or {})
            session.commit()
            return result


class AsyncDatabaseManager:
    """
    Manager asíncrono para conexiones a base de datos.
    Usado por la aplicación (FastAPI, etc.).
    """
    
    def __init__(self, database_url: str = None, echo: bool = False, **pool_kwargs):
        self.database_url = database_url or DatabaseConfig.get_database_url(async_mode=True)
        self.schema = DatabaseConfig.get_schema()
        self.defined_schemas = DatabaseConfig.get_defined_schemas()
        
        # Configurar asyncpg con server_settings para search_path
        connect_args = {
            "server_settings": {
                "search_path": f"{','.join(self.defined_schemas)},public"
            }
        }
        
        self.engine = create_async_engine(
            self.database_url,
            poolclass=AsyncAdaptedQueuePool,
            echo=echo,
            connect_args=connect_args,
            **pool_kwargs
        )
        
        self.session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
    
    async def close(self):
        """Cierra el engine"""
        await self.engine.dispose()
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Context manager asíncrono para sesiones de base de datos"""
        async with self.session_maker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Generator asíncrono para dependencias (estilo FastAPI)"""
        async with self.session_maker() as session:
            try:
                yield session
            finally:
                await session.close()
    
    async def init_database(self):
        """Inicializa la base de datos: extensiones, schemas, etc."""
        async with self.session() as session:
            # Verificar conexión
            await session.execute(text("SELECT 1"))
            
            # Extensiones PostGIS
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
            await session.execute(text("CREATE EXTENSION IF NOT EXISTS postgis_topology"))
            
            # Crear schemas definidos
            for schema in self.defined_schemas:
                await session.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            
            # Configurar search_path
            search_path = ','.join(self.defined_schemas) + ',public'
            await session.execute(text(f"SET search_path TO {search_path}"))
            
            await session.commit()


# Factory functions para crear managers fácilmente

def create_sync_manager(echo: bool = False) -> SyncDatabaseManager:
    """Crea un manager síncrono con configuración por defecto"""
    return SyncDatabaseManager(echo=echo)


def create_async_manager(echo: bool = False) -> AsyncDatabaseManager:
    """Crea un manager asíncrono con configuración por defecto"""
    return AsyncDatabaseManager(echo=echo)