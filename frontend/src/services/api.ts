import axios, { AxiosInstance, AxiosResponse } from 'axios';
import {
  StockInfo,
  FinancialData,
  HistoricalData,
  FinancialScore,
  ScreeningRequest,
  ScreeningResponse,
  SearchResult,
  ApiError
} from '../types/stock';

// APIベースURL
const BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8000/api';

// Axiosインスタンスの作成
const apiClient: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// レスポンスインターセプターでエラーハンドリング
apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    console.error('API Error:', error);
    
    if (error.response?.data) {
      // サーバーからのエラーレスポンス
      throw new Error(error.response.data.detail || error.response.data.error || 'API Error');
    } else if (error.request) {
      // リクエストは送信されたが、レスポンスがない
      throw new Error('サーバーに接続できません。ネットワーク接続を確認してください。');
    } else {
      // その他のエラー
      throw new Error('予期しないエラーが発生しました。');
    }
  }
);

// APIサービスクラス
export class StockAPIService {
  
  /**
   * 株式の基本情報を取得
   */
  static async getStockInfo(symbol: string): Promise<StockInfo> {
    try {
      const response = await apiClient.get<StockInfo>(`/stocks/info/${symbol}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching stock info for ${symbol}:`, error);
      throw error;
    }
  }

  /**
   * 株式の財務データを取得
   */
  static async getFinancialData(symbol: string): Promise<FinancialData> {
    try {
      const response = await apiClient.get<FinancialData>(`/stocks/financial/${symbol}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching financial data for ${symbol}:`, error);
      throw error;
    }
  }

  /**
   * 株式の履歴データを取得
   */
  static async getHistoricalData(symbol: string, period: string = '1y'): Promise<HistoricalData> {
    try {
      const response = await apiClient.get<HistoricalData>(`/stocks/history/${symbol}`, {
        params: { period }
      });
      return response.data;
    } catch (error) {
      console.error(`Error fetching historical data for ${symbol}:`, error);
      throw error;
    }
  }

  /**
   * 株式の財務スコアを取得
   */
  static async getFinancialScore(symbol: string): Promise<FinancialScore> {
    try {
      const response = await apiClient.get<FinancialScore>(`/stocks/score/${symbol}`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching financial score for ${symbol}:`, error);
      throw error;
    }
  }

  /**
   * 株式スクリーニングを実行
   */
  static async screenStocks(request: ScreeningRequest): Promise<ScreeningResponse> {
    try {
      const response = await apiClient.post<ScreeningResponse>('/stocks/screening', request);
      return response.data;
    } catch (error) {
      console.error('Error screening stocks:', error);
      throw error;
    }
  }

  /**
   * 株式を検索
   */
  static async searchStocks(query: string, limit: number = 10): Promise<SearchResult[]> {
    try {
      const response = await apiClient.get<{results: SearchResult[]}>('/stocks/search', {
        params: { query, limit }
      });
      return response.data.results;
    } catch (error) {
      console.error('Error searching stocks:', error);
      throw error;
    }
  }

  /**
   * APIヘルスチェック
   */
  static async healthCheck(): Promise<{status: string, api: string}> {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * 複数の株式の基本情報を一括取得
   */
  static async getBatchStockInfo(symbols: string[]): Promise<StockInfo[]> {
    try {
      const promises = symbols.map(symbol => this.getStockInfo(symbol));
      const results = await Promise.allSettled(promises);
      
      return results
        .filter((result): result is PromiseFulfilledResult<StockInfo> => result.status === 'fulfilled')
        .map(result => result.value);
    } catch (error) {
      console.error('Error fetching batch stock info:', error);
      throw error;
    }
  }

  /**
   * 複数の株式の財務スコアを一括取得
   */
  static async getBatchFinancialScores(symbols: string[]): Promise<FinancialScore[]> {
    try {
      const promises = symbols.map(symbol => this.getFinancialScore(symbol));
      const results = await Promise.allSettled(promises);
      
      return results
        .filter((result): result is PromiseFulfilledResult<FinancialScore> => result.status === 'fulfilled')
        .map(result => result.value);
    } catch (error) {
      console.error('Error fetching batch financial scores:', error);
      throw error;
    }
  }
}

// ユーティリティ関数
export const formatCurrency = (value: number | undefined): string => {
  if (value === undefined || value === null) return 'N/A';
  
  if (value >= 1e12) {
    return `$${(value / 1e12).toFixed(2)}T`;
  } else if (value >= 1e9) {
    return `$${(value / 1e9).toFixed(2)}B`;
  } else if (value >= 1e6) {
    return `$${(value / 1e6).toFixed(2)}M`;
  } else if (value >= 1e3) {
    return `$${(value / 1e3).toFixed(2)}K`;
  } else {
    return `$${value.toFixed(2)}`;
  }
};

export const formatPercentage = (value: number | undefined): string => {
  if (value === undefined || value === null) return 'N/A';
  return `${(value * 100).toFixed(2)}%`;
};

export const formatNumber = (value: number | undefined, decimals: number = 2): string => {
  if (value === undefined || value === null) return 'N/A';
  return value.toFixed(decimals);
};

export const formatVolume = (value: number | undefined): string => {
  if (value === undefined || value === null) return 'N/A';
  
  if (value >= 1e9) {
    return `${(value / 1e9).toFixed(2)}B`;
  } else if (value >= 1e6) {
    return `${(value / 1e6).toFixed(2)}M`;
  } else if (value >= 1e3) {
    return `${(value / 1e3).toFixed(2)}K`;
  } else {
    return value.toString();
  }
};

// デフォルトエクスポート
export default StockAPIService;