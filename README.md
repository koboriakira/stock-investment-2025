# StockScreener - 株式分析ツール

Yahoo Finance APIを使用して「リスク小さく値上がりする株」をスクリーニングする株式分析ツールです。

## 機能

- 株式の基本的な財務指標分析
- 複数の指標による株式スクリーニング
- リスク評価と成長性分析
- 財務健全性スコア算出

## 技術スタック

### バックエンド
- Python 3.11
- FastAPI
- SQLite
- yfinance (Yahoo Finance API)

### フロントエンド
- React 18
- TypeScript
- Material-UI

### 開発環境
- Docker & Docker Compose

## セットアップ

### 前提条件
- Docker Desktop
- Docker Compose

### 起動方法

1. リポジトリをクローン
```bash
git clone [repository-url]
cd stock-investment-2025
```

2. 環境変数の設定
```bash
cp .env.example .env
```

3. Docker Composeで起動
```bash
docker-compose up --build
```

4. アクセス
- フロントエンド: http://localhost:3000
- バックエンドAPI: http://localhost:8000
- API文書: http://localhost:8000/docs

## 使用方法

1. 株式ティッカーシンボル（例: AAPL, MSFT）を入力
2. 財務指標を確認
3. スクリーニング条件を設定
4. 分析結果を確認

## 開発

### バックエンド開発
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### フロントエンド開発
```bash
cd frontend
npm install
npm start
```

## プロジェクト構造

```
stock-investment-2025/
├── backend/
│   ├── app/
│   │   ├── models/          # データモデル
│   │   ├── routes/          # APIルート
│   │   ├── services/        # ビジネスロジック
│   │   └── database/        # データベース設定
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # Reactコンポーネント
│   │   ├── services/        # API呼び出し
│   │   └── types/           # TypeScript型定義
│   ├── Dockerfile
│   └── package.json
├── database/                # SQLiteデータベース
├── docker-compose.yml
└── README.md
```

## 免責事項

本ツールは教育・研究目的で作成されており、投資助言を提供するものではありません。
投資判断は自己責任で行ってください。