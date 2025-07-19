from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class StockInfoResponse(BaseModel):
    """株式基本情報のレスポンススキーマ"""
    symbol: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    current_price: Optional[float] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    profit_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None
    volume: Optional[int] = None
    average_volume: Optional[int] = None
    shares_outstanding: Optional[int] = None
    float_shares: Optional[int] = None
    last_updated: str

class FinancialDataResponse(BaseModel):
    """財務データのレスポンススキーマ"""
    symbol: str
    financials: Dict[str, Any]
    balance_sheet: Dict[str, Any]
    cashflow: Dict[str, Any]
    last_updated: str

class HistoricalDataResponse(BaseModel):
    """履歴データのレスポンススキーマ"""
    symbol: str
    period: str
    data: List[Dict[str, Any]]
    last_updated: str

class FinancialScoreResponse(BaseModel):
    """財務スコアのレスポンススキーマ"""
    symbol: str
    overall_score: float = Field(..., ge=0, le=10, description="総合スコア (0-10)")
    detailed_scores: Dict[str, float]
    last_updated: str

class StockRequest(BaseModel):
    """株式情報取得リクエストスキーマ"""
    symbol: str = Field(..., min_length=1, max_length=10, description="株式ティッカーシンボル")

class HistoricalDataRequest(BaseModel):
    """履歴データ取得リクエストスキーマ"""
    symbol: str = Field(..., min_length=1, max_length=10, description="株式ティッカーシンボル")
    period: str = Field(default="1y", description="取得期間 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")

class ScreeningRequest(BaseModel):
    """スクリーニングリクエストスキーマ"""
    symbols: List[str] = Field(..., min_items=1, max_items=50, description="株式ティッカーシンボルのリスト")
    min_market_cap: Optional[float] = Field(None, ge=0, description="最小時価総額")
    max_pe_ratio: Optional[float] = Field(None, ge=0, description="最大PER")
    min_roe: Optional[float] = Field(None, ge=0, description="最小ROE")
    max_debt_to_equity: Optional[float] = Field(None, ge=0, description="最大負債比率")
    min_current_ratio: Optional[float] = Field(None, ge=0, description="最小流動比率")

class ScreeningResult(BaseModel):
    """スクリーニング結果のアイテム"""
    symbol: str
    name: str
    score: float
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    roe: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    meets_criteria: bool

class ScreeningResponse(BaseModel):
    """スクリーニングレスポンススキーマ"""
    request_id: str
    total_symbols: int
    passed_symbols: int
    results: List[ScreeningResult]
    execution_time: float
    last_updated: str

class ErrorResponse(BaseModel):
    """エラーレスポンススキーマ"""
    error: str
    detail: Optional[str] = None
    timestamp: str