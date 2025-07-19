from fastapi import APIRouter
from .stocks import router as stocks_router

# メインAPIルーター
api_router = APIRouter()

# 基本的なテストエンドポイント
@api_router.get("/")
async def api_root():
    return {"message": "StockScreener API", "status": "running"}

# ヘルスチェック
@api_router.get("/health")
async def api_health():
    return {"status": "healthy", "api": "running"}

# 株式関連のルートを追加
api_router.include_router(stocks_router, prefix="/stocks", tags=["stocks"])

# 将来的に追加するルートはここでインポートする
# from .screening import router as screening_router
# api_router.include_router(screening_router, prefix="/screening", tags=["screening"])

__all__ = ["api_router"]