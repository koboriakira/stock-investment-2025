import yfinance as yf
import pandas as pd
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging

from app.config import settings
from app.services.mock_data_service import mock_data_service

logger = logging.getLogger(__name__)

class YahooFinanceService:
    """Yahoo Finance APIを使用した株式データ取得サービス"""
    
    def __init__(self):
        self.rate_limit = settings.YAHOO_API_RATE_LIMIT
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        株式の基本情報を取得
        
        Args:
            symbol: 株式ティッカーシンボル
            
        Returns:
            株式情報の辞書、取得失敗時はNone
        """
        try:
            # まずモックデータを試す（開発環境用）
            mock_info = mock_data_service.get_stock_info(symbol)
            if mock_info:
                return self._format_stock_data(symbol, mock_info)
            
            # Yahoo Finance APIを使用
            loop = asyncio.get_event_loop()
            stock = await loop.run_in_executor(
                self.executor,
                self._get_stock_data,
                symbol
            )
            
            if stock is None:
                return None
            
            # 基本情報の取得
            info = stock.info
            
            return self._format_stock_data(symbol, info)
            
        except Exception as e:
            logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
            return None
    
    async def get_financial_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        株式の財務データを取得
        
        Args:
            symbol: 株式ティッカーシンボル
            
        Returns:
            財務データの辞書、取得失敗時はNone
        """
        try:
            # まずモックデータを試す（開発環境用）
            mock_data = mock_data_service.get_financial_data(symbol)
            if mock_data:
                return mock_data
                
            loop = asyncio.get_event_loop()
            stock = await loop.run_in_executor(
                self.executor,
                self._get_stock_data,
                symbol
            )
            
            if stock is None:
                return None
            
            # 財務データの取得
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow
            
            # データが存在しない場合はNoneを返す
            if financials.empty and balance_sheet.empty and cashflow.empty:
                return None
            
            financial_data = {
                "symbol": symbol.upper(),
                "financials": self._dataframe_to_dict(financials),
                "balance_sheet": self._dataframe_to_dict(balance_sheet),
                "cashflow": self._dataframe_to_dict(cashflow),
                "last_updated": datetime.now().isoformat()
            }
            
            return financial_data
            
        except Exception as e:
            logger.error(f"Error fetching financial data for {symbol}: {str(e)}")
            return None
    
    async def get_historical_data(
        self, 
        symbol: str, 
        period: str = "1y"
    ) -> Optional[Dict[str, Any]]:
        """
        株式の履歴データを取得
        
        Args:
            symbol: 株式ティッカーシンボル
            period: 取得期間 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            
        Returns:
            履歴データの辞書、取得失敗時はNone
        """
        try:
            # まずモックデータを試す（開発環境用）
            mock_data = mock_data_service.get_historical_data(symbol, period)
            if mock_data:
                return mock_data
                
            loop = asyncio.get_event_loop()
            stock = await loop.run_in_executor(
                self.executor,
                self._get_stock_data,
                symbol
            )
            
            if stock is None:
                return None
            
            # 履歴データの取得
            history = stock.history(period=period)
            
            if history.empty:
                return None
            
            # データフレームを辞書に変換
            history_dict = history.to_dict('records')
            
            # 日付をISO形式に変換
            for record in history_dict:
                if 'Date' in record:
                    record['Date'] = record['Date'].isoformat()
            
            return {
                "symbol": symbol.upper(),
                "period": period,
                "data": history_dict,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {str(e)}")
            return None
    
    async def calculate_financial_score(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        財務健全性スコアを計算
        
        Args:
            symbol: 株式ティッカーシンボル
            
        Returns:
            財務スコアの辞書、取得失敗時はNone
        """
        try:
            stock_info = await self.get_stock_info(symbol)
            if not stock_info:
                return None
            
            # 各指標のスコア計算（0-10のスケール）
            scores = {}
            
            # 負債比率スコア（低いほど良い）
            debt_equity = stock_info.get("debt_to_equity")
            if debt_equity is not None:
                scores["debt_score"] = max(0, 10 - (debt_equity / 100 * 10))
            
            # ROEスコア（高いほど良い）
            roe = stock_info.get("roe")
            if roe is not None:
                scores["roe_score"] = min(10, roe * 100)
            
            # 流動比率スコア（2.0が理想）
            current_ratio = stock_info.get("current_ratio")
            if current_ratio is not None:
                scores["liquidity_score"] = max(0, 10 - abs(current_ratio - 2.0) * 2)
            
            # PERスコア（適正レンジ10-20）
            pe_ratio = stock_info.get("pe_ratio")
            if pe_ratio is not None:
                if 10 <= pe_ratio <= 20:
                    scores["pe_score"] = 10
                elif pe_ratio < 10:
                    scores["pe_score"] = 8
                else:
                    scores["pe_score"] = max(0, 10 - (pe_ratio - 20) / 5)
            
            # 利益率スコア
            profit_margin = stock_info.get("profit_margin")
            if profit_margin is not None:
                scores["profit_score"] = min(10, profit_margin * 100)
            
            # 総合スコア計算
            valid_scores = [score for score in scores.values() if score is not None]
            overall_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0
            
            return {
                "symbol": symbol.upper(),
                "overall_score": round(overall_score, 2),
                "detailed_scores": scores,
                "last_updated": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error calculating financial score for {symbol}: {str(e)}")
            return None
    
    def _get_stock_data(self, symbol: str) -> Optional[yf.Ticker]:
        """
        yfinanceを使用して株式データを取得（同期関数）
        """
        try:
            stock = yf.Ticker(symbol)
            # データの存在確認 - infoが空辞書や不正な場合をチェック
            info = stock.info
            if not info or len(info) < 5:  # 最小限のフィールドが存在するかチェック
                logger.warning(f"Insufficient data for symbol {symbol}")
                return None
            
            # シンボルが実際に存在するかの確認
            if info.get('regularMarketPrice') is None and info.get('currentPrice') is None:
                logger.warning(f"No price data found for symbol {symbol}")
                return None
                
            return stock
        except Exception as e:
            logger.error(f"Error creating ticker for {symbol}: {str(e)}")
            return None
    
    def _format_stock_data(self, symbol: str, info: Dict[str, Any]) -> Dict[str, Any]:
        """
        株式データを統一フォーマットに変換
        """
        return {
            "symbol": symbol.upper(),
            "name": info.get("longName", info.get("shortName", "N/A")),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "market_cap": info.get("marketCap"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "pe_ratio": info.get("forwardPE") or info.get("trailingPE"),
            "pb_ratio": info.get("priceToBook"),
            "peg_ratio": info.get("pegRatio"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "debt_to_equity": info.get("debtToEquity"),
            "current_ratio": info.get("currentRatio"),
            "quick_ratio": info.get("quickRatio"),
            "gross_margin": info.get("grossMargins"),
            "operating_margin": info.get("operatingMargins"),
            "profit_margin": info.get("profitMargins"),
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "volume": info.get("volume") or info.get("regularMarketVolume"),
            "average_volume": info.get("averageVolume"),
            "shares_outstanding": info.get("sharesOutstanding"),
            "float_shares": info.get("floatShares"),
            "last_updated": datetime.now().isoformat()
        }
    
    def _dataframe_to_dict(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        DataFrameを辞書に変換
        """
        try:
            if df.empty:
                return {}
            
            # インデックスを文字列に変換
            df_copy = df.copy()
            df_copy.index = df_copy.index.astype(str)
            
            # 列名を文字列に変換
            df_copy.columns = df_copy.columns.astype(str)
            
            return df_copy.to_dict()
        except Exception as e:
            logger.error(f"Error converting dataframe to dict: {str(e)}")
            return {}

# サービスインスタンス
yahoo_finance_service = YahooFinanceService()