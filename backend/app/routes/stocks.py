from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from datetime import datetime
import uuid
import time
import logging

from app.schemas.stock import (
    StockInfoResponse,
    FinancialDataResponse,
    HistoricalDataResponse,
    FinancialScoreResponse,
    StockRequest,
    HistoricalDataRequest,
    ScreeningRequest,
    ScreeningResponse,
    ScreeningResult,
    ErrorResponse
)
from app.services.yahoo_finance_service import yahoo_finance_service
from app.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/info/{symbol}", response_model=StockInfoResponse)
async def get_stock_info(symbol: str):
    """
    株式の基本情報を取得
    
    Args:
        symbol: 株式ティッカーシンボル
        
    Returns:
        株式の基本情報
    """
    try:
        stock_info = await yahoo_finance_service.get_stock_info(symbol)
        if not stock_info:
            raise HTTPException(
                status_code=404,
                detail=f"株式 '{symbol}' の情報が見つかりません"
            )
        
        return StockInfoResponse(**stock_info)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stock info for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="株式情報の取得中にエラーが発生しました"
        )

@router.get("/financial/{symbol}", response_model=FinancialDataResponse)
async def get_financial_data(symbol: str):
    """
    株式の財務データを取得
    
    Args:
        symbol: 株式ティッカーシンボル
        
    Returns:
        財務データ
    """
    try:
        financial_data = await yahoo_finance_service.get_financial_data(symbol)
        if not financial_data:
            raise HTTPException(
                status_code=404,
                detail=f"株式 '{symbol}' の財務データが見つかりません"
            )
        
        return FinancialDataResponse(**financial_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting financial data for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="財務データの取得中にエラーが発生しました"
        )

@router.get("/history/{symbol}", response_model=HistoricalDataResponse)
async def get_historical_data(
    symbol: str,
    period: str = Query(default="1y", description="取得期間 (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)")
):
    """
    株式の履歴データを取得
    
    Args:
        symbol: 株式ティッカーシンボル
        period: 取得期間
        
    Returns:
        履歴データ
    """
    try:
        # 有効な期間かチェック
        valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"無効な期間です。有効な期間: {', '.join(valid_periods)}"
            )
        
        historical_data = await yahoo_finance_service.get_historical_data(symbol, period)
        if not historical_data:
            raise HTTPException(
                status_code=404,
                detail=f"株式 '{symbol}' の履歴データが見つかりません"
            )
        
        return HistoricalDataResponse(**historical_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting historical data for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="履歴データの取得中にエラーが発生しました"
        )

@router.get("/score/{symbol}", response_model=FinancialScoreResponse)
async def get_financial_score(symbol: str):
    """
    株式の財務健全性スコアを取得
    
    Args:
        symbol: 株式ティッカーシンボル
        
    Returns:
        財務健全性スコア
    """
    try:
        score_data = await yahoo_finance_service.calculate_financial_score(symbol)
        if not score_data:
            raise HTTPException(
                status_code=404,
                detail=f"株式 '{symbol}' のスコア計算ができませんでした"
            )
        
        return FinancialScoreResponse(**score_data)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error calculating financial score for {symbol}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="財務スコアの計算中にエラーが発生しました"
        )

@router.post("/screening", response_model=ScreeningResponse)
async def screen_stocks(request: ScreeningRequest):
    """
    複数の株式をスクリーニング
    
    Args:
        request: スクリーニングリクエスト
        
    Returns:
        スクリーニング結果
    """
    try:
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        # 最大数制限チェック
        if len(request.symbols) > settings.MAX_STOCKS_PER_REQUEST:
            raise HTTPException(
                status_code=400,
                detail=f"一度に処理できる株式数は{settings.MAX_STOCKS_PER_REQUEST}件までです"
            )
        
        results = []
        passed_count = 0
        
        for symbol in request.symbols:
            try:
                # 株式情報を取得
                stock_info = await yahoo_finance_service.get_stock_info(symbol)
                if not stock_info:
                    continue
                
                # 財務スコアを計算
                score_data = await yahoo_finance_service.calculate_financial_score(symbol)
                
                # スクリーニング条件をチェック
                meets_criteria = True
                
                if request.min_market_cap and stock_info.get("market_cap"):
                    if stock_info["market_cap"] < request.min_market_cap:
                        meets_criteria = False
                
                if request.max_pe_ratio and stock_info.get("pe_ratio"):
                    if stock_info["pe_ratio"] > request.max_pe_ratio:
                        meets_criteria = False
                
                if request.min_roe and stock_info.get("roe"):
                    if stock_info["roe"] < request.min_roe:
                        meets_criteria = False
                
                if request.max_debt_to_equity and stock_info.get("debt_to_equity"):
                    if stock_info["debt_to_equity"] > request.max_debt_to_equity:
                        meets_criteria = False
                
                if request.min_current_ratio and stock_info.get("current_ratio"):
                    if stock_info["current_ratio"] < request.min_current_ratio:
                        meets_criteria = False
                
                if meets_criteria:
                    passed_count += 1
                
                # 結果を追加
                result = ScreeningResult(
                    symbol=symbol,
                    name=stock_info.get("name", "N/A"),
                    score=score_data.get("overall_score", 0) if score_data else 0,
                    market_cap=stock_info.get("market_cap"),
                    pe_ratio=stock_info.get("pe_ratio"),
                    roe=stock_info.get("roe"),
                    debt_to_equity=stock_info.get("debt_to_equity"),
                    current_ratio=stock_info.get("current_ratio"),
                    meets_criteria=meets_criteria
                )
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Error screening stock {symbol}: {str(e)}")
                continue
        
        # 結果をスコア順でソート
        results.sort(key=lambda x: x.score, reverse=True)
        
        execution_time = time.time() - start_time
        
        response = ScreeningResponse(
            request_id=request_id,
            total_symbols=len(request.symbols),
            passed_symbols=passed_count,
            results=results,
            execution_time=execution_time,
            last_updated=datetime.now().isoformat()
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during screening: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="スクリーニング中にエラーが発生しました"
        )

@router.get("/search")
async def search_stocks(
    query: str = Query(..., min_length=1, description="検索クエリ"),
    limit: int = Query(default=10, ge=1, le=50, description="結果数の制限")
):
    """
    株式を検索（将来的な実装用プレースホルダー）
    
    Args:
        query: 検索クエリ
        limit: 結果数の制限
        
    Returns:
        検索結果
    """
    # 現在は単純な実装
    # 実際のプロダクションでは、株式リストデータベースや外部APIを使用
    return {
        "query": query,
        "results": [
            {"symbol": "AAPL", "name": "Apple Inc.", "relevance": 0.95},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "relevance": 0.85},
        ],
        "total": 2,
        "limit": limit
    }