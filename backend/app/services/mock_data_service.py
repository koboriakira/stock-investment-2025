"""
モックデータサービス - Yahoo Finance APIの代替として使用
開発・テスト目的で使用
"""
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import random


class MockDataService:
    """モックデータを提供するサービス"""
    
    def __init__(self):
        self.mock_stocks = {
            "AAPL": {
                "longName": "Apple Inc.",
                "shortName": "Apple",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "marketCap": 2800000000000,
                "currentPrice": 190.50,
                "regularMarketPrice": 190.50,
                "forwardPE": 28.5,
                "trailingPE": 30.2,
                "priceToBook": 45.8,
                "pegRatio": 2.1,
                "dividendYield": 0.0044,
                "beta": 1.25,
                "returnOnEquity": 1.479,
                "returnOnAssets": 0.229,
                "debtToEquity": 195.0,
                "currentRatio": 1.04,
                "quickRatio": 0.95,
                "grossMargins": 0.381,
                "operatingMargins": 0.297,
                "profitMargins": 0.246,
                "revenueGrowth": 0.023,
                "earningsGrowth": 0.11,
                "fiftyTwoWeekHigh": 199.62,
                "fiftyTwoWeekLow": 164.08,
                "volume": 45678901,
                "regularMarketVolume": 45678901,
                "averageVolume": 52000000,
                "sharesOutstanding": 15728700000,
                "floatShares": 15700000000
            },
            "MSFT": {
                "longName": "Microsoft Corporation",
                "shortName": "Microsoft",
                "sector": "Technology",
                "industry": "Software—Infrastructure",
                "marketCap": 2600000000000,
                "currentPrice": 350.20,
                "regularMarketPrice": 350.20,
                "forwardPE": 25.8,
                "trailingPE": 28.5,
                "priceToBook": 12.5,
                "pegRatio": 1.8,
                "dividendYield": 0.0072,
                "beta": 0.89,
                "returnOnEquity": 0.428,
                "returnOnAssets": 0.168,
                "debtToEquity": 47.0,
                "currentRatio": 1.77,
                "quickRatio": 1.75,
                "grossMargins": 0.688,
                "operatingMargins": 0.424,
                "profitMargins": 0.362,
                "revenueGrowth": 0.127,
                "earningsGrowth": 0.095,
                "fiftyTwoWeekHigh": 384.30,
                "fiftyTwoWeekLow": 213.43,
                "volume": 23456789,
                "regularMarketVolume": 23456789,
                "averageVolume": 28000000,
                "sharesOutstanding": 7430000000,
                "floatShares": 7425000000
            },
            "GOOGL": {
                "longName": "Alphabet Inc.",
                "shortName": "Alphabet",
                "sector": "Technology",
                "industry": "Internet Content & Information",
                "marketCap": 1700000000000,
                "currentPrice": 135.85,
                "regularMarketPrice": 135.85,
                "forwardPE": 22.1,
                "trailingPE": 25.6,
                "priceToBook": 5.8,
                "pegRatio": 1.4,
                "dividendYield": None,
                "beta": 1.05,
                "returnOnEquity": 0.276,
                "returnOnAssets": 0.134,
                "debtToEquity": 14.8,
                "currentRatio": 2.85,
                "quickRatio": 2.85,
                "grossMargins": 0.548,
                "operatingMargins": 0.278,
                "profitMargins": 0.211,
                "revenueGrowth": 0.071,
                "earningsGrowth": 0.089,
                "fiftyTwoWeekHigh": 153.78,
                "fiftyTwoWeekLow": 83.34,
                "volume": 34567890,
                "regularMarketVolume": 34567890,
                "averageVolume": 31000000,
                "sharesOutstanding": 12900000000,
                "floatShares": 12850000000
            },
            # 日本株のサンプル
            "6758.T": {
                "longName": "ソニーグループ株式会社",
                "shortName": "ソニーG",
                "sector": "Technology",
                "industry": "Consumer Electronics",
                "marketCap": 12000000000000,
                "currentPrice": 12500.0,
                "regularMarketPrice": 12500.0,
                "forwardPE": 15.8,
                "trailingPE": 17.2,
                "priceToBook": 1.8,
                "pegRatio": 1.2,
                "dividendYield": 0.006,
                "beta": 1.15,
                "returnOnEquity": 0.125,
                "returnOnAssets": 0.078,
                "debtToEquity": 42.0,
                "currentRatio": 1.35,
                "quickRatio": 1.15,
                "grossMargins": 0.425,
                "operatingMargins": 0.135,
                "profitMargins": 0.098,
                "revenueGrowth": 0.089,
                "earningsGrowth": 0.145,
                "fiftyTwoWeekHigh": 13850.0,
                "fiftyTwoWeekLow": 9850.0,
                "volume": 8765432,
                "regularMarketVolume": 8765432,
                "averageVolume": 12000000,
                "sharesOutstanding": 1240000000,
                "floatShares": 1235000000
            },
            "9984.T": {
                "longName": "ソフトバンクグループ株式会社",
                "shortName": "SBG",
                "sector": "Technology",
                "industry": "Telecom Services",
                "marketCap": 8500000000000,
                "currentPrice": 5850.0,
                "regularMarketPrice": 5850.0,
                "forwardPE": 12.5,
                "trailingPE": 14.8,
                "priceToBook": 0.95,
                "pegRatio": 0.9,
                "dividendYield": 0.012,
                "beta": 1.45,
                "returnOnEquity": 0.068,
                "returnOnAssets": 0.028,
                "debtToEquity": 185.0,
                "currentRatio": 1.08,
                "quickRatio": 0.95,
                "grossMargins": 0.385,
                "operatingMargins": 0.125,
                "profitMargins": 0.065,
                "revenueGrowth": 0.045,
                "earningsGrowth": 0.089,
                "fiftyTwoWeekHigh": 6980.0,
                "fiftyTwoWeekLow": 4750.0,
                "volume": 15678901,
                "regularMarketVolume": 15678901,
                "averageVolume": 18000000,
                "sharesOutstanding": 1500000000,
                "floatShares": 1485000000
            },
            "7203.T": {
                "longName": "トヨタ自動車株式会社",
                "shortName": "トヨタ",
                "sector": "Consumer Cyclical",
                "industry": "Auto Manufacturers",
                "marketCap": 25000000000000,
                "currentPrice": 2850.0,
                "regularMarketPrice": 2850.0,
                "forwardPE": 9.2,
                "trailingPE": 10.5,
                "priceToBook": 0.85,
                "pegRatio": 0.8,
                "dividendYield": 0.025,
                "beta": 0.65,
                "returnOnEquity": 0.089,
                "returnOnAssets": 0.045,
                "debtToEquity": 85.0,
                "currentRatio": 1.15,
                "quickRatio": 0.95,
                "grossMargins": 0.198,
                "operatingMargins": 0.089,
                "profitMargins": 0.078,
                "revenueGrowth": 0.067,
                "earningsGrowth": 0.112,
                "fiftyTwoWeekHigh": 3045.0,
                "fiftyTwoWeekLow": 2156.0,
                "volume": 12345678,
                "regularMarketVolume": 12345678,
                "averageVolume": 15000000,
                "sharesOutstanding": 14720000000,
                "floatShares": 14700000000
            }
        }
    
    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        モック株式情報を取得
        
        Args:
            symbol: 株式ティッカーシンボル
            
        Returns:
            株式情報の辞書、存在しない場合はNone
        """
        symbol = symbol.upper()
        if symbol in self.mock_stocks:
            return self.mock_stocks[symbol].copy()
        return None
    
    def get_financial_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        モック財務データを取得
        
        Args:
            symbol: 株式ティッカーシンボル
            
        Returns:
            財務データの辞書、存在しない場合はNone
        """
        # 簡単なモック財務データ
        if symbol.upper() in self.mock_stocks:
            return {
                "symbol": symbol.upper(),
                "financials": {
                    "2023": {"Revenue": 383285000000, "NetIncome": 96995000000},
                    "2022": {"Revenue": 394328000000, "NetIncome": 99803000000},
                    "2021": {"Revenue": 365817000000, "NetIncome": 94680000000}
                },
                "balance_sheet": {
                    "2023": {"TotalAssets": 352755000000, "TotalDebt": 123930000000},
                    "2022": {"TotalAssets": 352583000000, "TotalDebt": 120069000000}
                },
                "cashflow": {
                    "2023": {"OperatingCashFlow": 110543000000, "FreeCashFlow": 84726000000},
                    "2022": {"OperatingCashFlow": 122151000000, "FreeCashFlow": 111443000000}
                },
                "last_updated": datetime.now().isoformat()
            }
        return None
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> Optional[Dict[str, Any]]:
        """
        モック履歴データを取得
        
        Args:
            symbol: 株式ティッカーシンボル
            period: 取得期間
            
        Returns:
            履歴データの辞書、存在しない場合はNone
        """
        if symbol.upper() not in self.mock_stocks:
            return None
        
        # 基準価格を取得
        base_price = self.mock_stocks[symbol.upper()]["currentPrice"]
        
        # 期間に応じた日数を決定
        period_days = {
            "1d": 1, "5d": 5, "1mo": 30, "3mo": 90,
            "6mo": 180, "1y": 365, "2y": 730, "5y": 1825
        }.get(period, 365)
        
        # モック履歴データを生成
        data = []
        current_date = datetime.now() - timedelta(days=period_days)
        current_price = base_price * 0.9  # 開始価格
        
        for i in range(period_days):
            # ランダムな価格変動を生成
            change = random.uniform(-0.05, 0.05)
            current_price = current_price * (1 + change)
            
            data.append({
                "Date": current_date.isoformat(),
                "Open": round(current_price * 0.998, 2),
                "High": round(current_price * 1.002, 2),
                "Low": round(current_price * 0.996, 2),
                "Close": round(current_price, 2),
                "Volume": random.randint(20000000, 80000000)
            })
            
            current_date += timedelta(days=1)
        
        return {
            "symbol": symbol.upper(),
            "period": period,
            "data": data,
            "last_updated": datetime.now().isoformat()
        }


# サービスインスタンス
mock_data_service = MockDataService()