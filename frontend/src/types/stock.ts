// 株式基本情報の型定義
export interface StockInfo {
  symbol: string;
  name: string;
  sector?: string;
  industry?: string;
  market_cap?: number;
  current_price?: number;
  pe_ratio?: number;
  pb_ratio?: number;
  peg_ratio?: number;
  dividend_yield?: number;
  beta?: number;
  roe?: number;
  roa?: number;
  debt_to_equity?: number;
  current_ratio?: number;
  quick_ratio?: number;
  gross_margin?: number;
  operating_margin?: number;
  profit_margin?: number;
  revenue_growth?: number;
  earnings_growth?: number;
  fifty_two_week_high?: number;
  fifty_two_week_low?: number;
  volume?: number;
  average_volume?: number;
  shares_outstanding?: number;
  float_shares?: number;
  last_updated: string;
}

// 財務データの型定義
export interface FinancialData {
  symbol: string;
  financials: Record<string, any>;
  balance_sheet: Record<string, any>;
  cashflow: Record<string, any>;
  last_updated: string;
}

// 履歴データの型定義
export interface HistoricalData {
  symbol: string;
  period: string;
  data: Array<{
    Date: string;
    Open: number;
    High: number;
    Low: number;
    Close: number;
    Volume: number;
  }>;
  last_updated: string;
}

// 財務スコアの型定義
export interface FinancialScore {
  symbol: string;
  overall_score: number;
  detailed_scores: {
    debt_score?: number;
    roe_score?: number;
    liquidity_score?: number;
    pe_score?: number;
    profit_score?: number;
  };
  last_updated: string;
}

// スクリーニングリクエストの型定義
export interface ScreeningRequest {
  symbols: string[];
  min_market_cap?: number;
  max_pe_ratio?: number;
  min_roe?: number;
  max_debt_to_equity?: number;
  min_current_ratio?: number;
}

// スクリーニング結果の型定義
export interface ScreeningResult {
  symbol: string;
  name: string;
  score: number;
  market_cap?: number;
  pe_ratio?: number;
  roe?: number;
  debt_to_equity?: number;
  current_ratio?: number;
  meets_criteria: boolean;
}

// スクリーニングレスポンスの型定義
export interface ScreeningResponse {
  request_id: string;
  total_symbols: number;
  passed_symbols: number;
  results: ScreeningResult[];
  execution_time: number;
  last_updated: string;
}

// API エラーレスポンスの型定義
export interface ApiError {
  error: string;
  detail?: string;
  timestamp: string;
}

// チャートデータの型定義
export interface ChartData {
  labels: string[];
  datasets: Array<{
    label: string;
    data: number[];
    borderColor: string;
    backgroundColor: string;
    fill: boolean;
  }>;
}

// ウォッチリストの型定義
export interface WatchListItem {
  id: number;
  symbol: string;
  name: string;
  current_price?: number;
  change?: number;
  change_percent?: number;
  target_price?: number;
  notes?: string;
  added_at: string;
}

// 検索結果の型定義
export interface SearchResult {
  symbol: string;
  name: string;
  relevance: number;
}

// APIレスポンスの汎用型
export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

// フィルター条件の型定義
export interface FilterConditions {
  minMarketCap?: number;
  maxPE?: number;
  minROE?: number;
  maxDebtToEquity?: number;
  minCurrentRatio?: number;
  sectors?: string[];
}

// ソート条件の型定義
export interface SortConditions {
  field: keyof StockInfo;
  direction: 'asc' | 'desc';
}

// ページネーションの型定義
export interface Pagination {
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}