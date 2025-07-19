from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import os

from app.config import settings

# データベースファイルのディレクトリを確実に作成
database_path = settings.DATABASE_URL.replace("sqlite:///", "")
database_dir = os.path.dirname(database_path)
os.makedirs(database_dir, exist_ok=True)

# 同期データベースエンジンの作成（テーブル作成用）
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=settings.ENVIRONMENT == "development"
)

# 非同期データベースエンジンの作成
async_database_url = settings.DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
async_engine = create_async_engine(
    async_database_url,
    echo=settings.ENVIRONMENT == "development"
)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# メタデータとベースクラス
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# 依存性注入用の関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 非同期データベースセッションの取得
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session