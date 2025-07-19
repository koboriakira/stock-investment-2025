from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class ScreeningSession(Base):
    """スクリーニングセッションテーブル"""
    __tablename__ = "screening_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(36), unique=True, index=True, nullable=False)  # UUID
    
    # スクリーニング条件
    min_market_cap = Column(Float)
    max_pe_ratio = Column(Float)
    min_roe = Column(Float)
    max_debt_to_equity = Column(Float)
    min_current_ratio = Column(Float)
    
    # 実行結果
    total_symbols = Column(Integer)
    passed_symbols = Column(Integer)
    execution_time = Column(Float)
    
    # メタデータ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    results = relationship("ScreeningResult", back_populates="session")
    
    def __repr__(self):
        return f"<ScreeningSession(session_id='{self.session_id}', passed_symbols={self.passed_symbols})>"

class ScreeningResult(Base):
    """スクリーニング結果テーブル"""
    __tablename__ = "screening_results"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("screening_sessions.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    
    # スクリーニング結果
    overall_score = Column(Float)
    meets_criteria = Column(Boolean)
    
    # 詳細スコア（JSON形式で保存）
    detailed_scores = Column(Text)
    
    # スクリーニング時の株式データ（スナップショット）
    market_cap_snapshot = Column(Float)
    pe_ratio_snapshot = Column(Float)
    roe_snapshot = Column(Float)
    debt_to_equity_snapshot = Column(Float)
    current_ratio_snapshot = Column(Float)
    
    # メタデータ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    session = relationship("ScreeningSession", back_populates="results")
    stock = relationship("Stock", back_populates="screening_results")
    
    def __repr__(self):
        return f"<ScreeningResult(stock_id={self.stock_id}, score={self.overall_score})>"

class WatchList(Base):
    """ウォッチリストテーブル"""
    __tablename__ = "watch_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # メタデータ
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーションシップ
    items = relationship("WatchListItem", back_populates="watch_list")
    
    def __repr__(self):
        return f"<WatchList(name='{self.name}')>"

class WatchListItem(Base):
    """ウォッチリストアイテムテーブル"""
    __tablename__ = "watch_list_items"
    
    id = Column(Integer, primary_key=True, index=True)
    watch_list_id = Column(Integer, ForeignKey("watch_lists.id"), nullable=False)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    
    # アイテム固有の設定
    notes = Column(Text)
    target_price = Column(Float)
    stop_loss_price = Column(Float)
    
    # メタデータ
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # リレーションシップ
    watch_list = relationship("WatchList", back_populates="items")
    stock = relationship("Stock", back_populates="watch_list_items")
    
    def __repr__(self):
        return f"<WatchListItem(watch_list_id={self.watch_list_id}, stock_id={self.stock_id})>"

# Stockモデルにリレーションシップを追加するため、後でインポートする際に使用
def add_stock_relationships():
    from app.models.stock import Stock
    Stock.screening_results = relationship("ScreeningResult", back_populates="stock")
    Stock.watch_list_items = relationship("WatchListItem", back_populates="stock")