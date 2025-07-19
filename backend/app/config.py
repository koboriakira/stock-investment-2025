from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os

class Settings(BaseSettings):
    # アプリケーション設定
    APP_NAME: str = Field(default="StockScreener", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", env="APP_VERSION")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    
    # データベース設定
    DATABASE_URL: str = Field(default="sqlite:///./database/stockscreener.db", env="DATABASE_URL")
    
    # API設定
    API_HOST: str = Field(default="0.0.0.0", env="API_HOST")
    API_PORT: int = Field(default=8000, env="API_PORT")
    API_RELOAD: bool = Field(default=True, env="API_RELOAD")
    
    # Yahoo Finance API設定
    YAHOO_API_RATE_LIMIT: int = Field(default=5, env="YAHOO_API_RATE_LIMIT")
    
    # ログ設定
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        env="LOG_FORMAT"
    )
    
    # スクリーニング設定
    DEFAULT_SCREENING_TIMEOUT: int = Field(default=30, env="DEFAULT_SCREENING_TIMEOUT")
    MAX_STOCKS_PER_REQUEST: int = Field(default=10, env="MAX_STOCKS_PER_REQUEST")
    
    # キャッシュ設定
    CACHE_EXPIRY_MINUTES: int = Field(default=60, env="CACHE_EXPIRY_MINUTES")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# グローバル設定インスタンス
settings = Settings()

# データベースURL（相対パス対応）
if settings.DATABASE_URL.startswith("sqlite:///./"):
    database_path = settings.DATABASE_URL.replace("sqlite:///./", "")
    if not os.path.isabs(database_path):
        # 相対パスの場合は絶対パスに変換
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        database_full_path = os.path.join(base_dir, database_path)
        settings.DATABASE_URL = f"sqlite:///{database_full_path}"