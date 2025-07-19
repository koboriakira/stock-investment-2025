"""
データベース初期化スクリプト
"""
import os
import logging
from sqlalchemy import create_engine
from app.database.connection import Base
from app.models import *  # 全てのモデルをインポート
from app.config import settings

logger = logging.getLogger(__name__)

def init_database():
    """
    データベースを初期化する
    """
    try:
        # データベースファイルのディレクトリを作成
        database_path = settings.DATABASE_URL.replace("sqlite:///", "")
        database_dir = os.path.dirname(database_path)
        if not os.path.exists(database_dir):
            os.makedirs(database_dir, exist_ok=True)
            logger.info(f"Created database directory: {database_dir}")
        
        # エンジンを作成
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
            echo=settings.ENVIRONMENT == "development"
        )
        
        # 全てのテーブルを作成
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        
        # サンプルデータを挿入（開発環境の場合）
        if settings.ENVIRONMENT == "development":
            create_sample_data(engine)
        
        return True
        
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

def create_sample_data(engine):
    """
    サンプルデータを作成する（開発環境用）
    """
    from sqlalchemy.orm import sessionmaker
    from app.models import Stock, WatchList
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # サンプル株式データ
        sample_stocks = [
            Stock(
                symbol="AAPL",
                name="Apple Inc.",
                sector="Technology",
                industry="Consumer Electronics",
                market_cap=3000000000000,
                current_price=150.00,
                pe_ratio=25.0,
                pb_ratio=8.0,
                dividend_yield=0.005,
                beta=1.2,
                roe=0.15,
                roa=0.12,
                debt_to_equity=0.3,
                current_ratio=1.5
            ),
            Stock(
                symbol="MSFT",
                name="Microsoft Corporation",
                sector="Technology",
                industry="Software",
                market_cap=2500000000000,
                current_price=350.00,
                pe_ratio=28.0,
                pb_ratio=12.0,
                dividend_yield=0.007,
                beta=0.9,
                roe=0.18,
                roa=0.14,
                debt_to_equity=0.2,
                current_ratio=2.0
            ),
            Stock(
                symbol="GOOGL",
                name="Alphabet Inc.",
                sector="Technology",
                industry="Internet Content & Information",
                market_cap=1800000000000,
                current_price=140.00,
                pe_ratio=22.0,
                pb_ratio=5.0,
                dividend_yield=0.0,
                beta=1.1,
                roe=0.20,
                roa=0.16,
                debt_to_equity=0.1,
                current_ratio=2.5
            )
        ]
        
        # 既存データがない場合のみ挿入
        existing_stocks = session.query(Stock).first()
        if not existing_stocks:
            session.add_all(sample_stocks)
            session.commit()
            logger.info("Sample stock data created")
        
        # サンプルウォッチリスト
        existing_watchlist = session.query(WatchList).first()
        if not existing_watchlist:
            watchlist = WatchList(
                name="テック株ウォッチリスト",
                description="主要テクノロジー株の監視リスト"
            )
            session.add(watchlist)
            session.commit()
            logger.info("Sample watchlist created")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {str(e)}")
        session.rollback()
    finally:
        session.close()

def drop_all_tables():
    """
    全てのテーブルを削除する（開発用）
    """
    try:
        engine = create_engine(
            settings.DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
        )
        
        Base.metadata.drop_all(bind=engine)
        logger.info("All tables dropped successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error dropping tables: {str(e)}")
        return False

def reset_database():
    """
    データベースをリセットする（開発用）
    """
    logger.info("Resetting database...")
    if drop_all_tables():
        return init_database()
    return False

if __name__ == "__main__":
    # スクリプトを直接実行した場合
    logging.basicConfig(level=logging.INFO)
    init_database()