from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base

class FinancialData(Base):
    """財務データテーブル"""
    __tablename__ = "financial_data"
    
    id = Column(Integer, primary_key=True, index=True)
    stock_id = Column(Integer, ForeignKey("stocks.id"), nullable=False)
    
    # 財務諸表データ（JSON形式で保存）
    financials = Column(Text)  # 損益計算書データ
    balance_sheet = Column(Text)  # 貸借対照表データ
    cashflow = Column(Text)  # キャッシュフロー計算書データ
    
    # 主要な財務指標（高速検索用）
    total_revenue = Column(Float)
    net_income = Column(Float)
    total_assets = Column(Float)
    total_debt = Column(Float)
    shareholders_equity = Column(Float)
    operating_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    
    # 計算されたメトリクス
    debt_to_equity_ratio = Column(Float)
    return_on_equity = Column(Float)
    return_on_assets = Column(Float)
    profit_margin = Column(Float)
    operating_margin = Column(Float)
    
    # メタデータ
    fiscal_year = Column(Integer)
    fiscal_quarter = Column(Integer)
    report_date = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # リレーションシップ
    stock = relationship("Stock", back_populates="financial_data")
    
    def __repr__(self):
        return f"<FinancialData(stock_id={self.stock_id}, fiscal_year={self.fiscal_year})>"

# Stockモデルにリレーションシップを追加するため、後でインポートする際に使用
def add_stock_relationship():
    from app.models.stock import Stock
    Stock.financial_data = relationship("FinancialData", back_populates="stock")