import React, { useState } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Alert,
  CircularProgress,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Divider,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  FilterList as FilterListIcon,
  Clear as ClearIcon,
  Download as DownloadIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';

import { StockAPIService, formatCurrency, formatPercentage, formatNumber } from '../services/api';
import { ScreeningRequest, ScreeningResponse, ScreeningResult } from '../types/stock';

const Screening: React.FC = () => {
  const [symbols, setSymbols] = useState<string>('');
  const [filters, setFilters] = useState({
    minMarketCap: '',
    maxPeRatio: '',
    minRoe: '',
    maxDebtToEquity: '',
    minCurrentRatio: '',
  });
  const [results, setResults] = useState<ScreeningResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleFilterChange = (field: keyof typeof filters) => (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFilters(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };

  const clearFilters = () => {
    setFilters({
      minMarketCap: '',
      maxPeRatio: '',
      minRoe: '',
      maxDebtToEquity: '',
      minCurrentRatio: '',
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symbols.trim()) {
      setError('株式ティッカーシンボルを入力してください');
      return;
    }

    const symbolList = symbols
      .split(',')
      .map(s => s.trim().toUpperCase())
      .filter(s => s.length > 0);

    if (symbolList.length === 0) {
      setError('有効な株式ティッカーシンボルを入力してください');
      return;
    }

    const request: ScreeningRequest = {
      symbols: symbolList,
      ...(filters.minMarketCap && { min_market_cap: parseFloat(filters.minMarketCap) }),
      ...(filters.maxPeRatio && { max_pe_ratio: parseFloat(filters.maxPeRatio) }),
      ...(filters.minRoe && { min_roe: parseFloat(filters.minRoe) / 100 }),
      ...(filters.maxDebtToEquity && { max_debt_to_equity: parseFloat(filters.maxDebtToEquity) }),
      ...(filters.minCurrentRatio && { min_current_ratio: parseFloat(filters.minCurrentRatio) }),
    };

    setLoading(true);
    setError(null);
    setResults(null);

    try {
      const response = await StockAPIService.screenStocks(request);
      setResults(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'スクリーニングに失敗しました');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'success';
    if (score >= 6) return 'warning';
    return 'error';
  };

  const getScoreIcon = (score: number) => {
    if (score >= 8) return <TrendingUpIcon fontSize="small" />;
    if (score >= 6) return <ShowChartIcon fontSize="small" />;
    return <TrendingDownIcon fontSize="small" />;
  };

  const exportResults = () => {
    if (!results) return;

    const csvContent = [
      ['Symbol', 'Name', 'Score', 'Market Cap', 'P/E Ratio', 'ROE', 'Debt/Equity', 'Current Ratio', 'Meets Criteria'].join(','),
      ...results.results.map(result => [
        result.symbol,
        `"${result.name}"`,
        result.score.toFixed(2),
        result.market_cap || 'N/A',
        result.pe_ratio || 'N/A',
        result.roe ? (result.roe * 100).toFixed(2) + '%' : 'N/A',
        result.debt_to_equity || 'N/A',
        result.current_ratio || 'N/A',
        result.meets_criteria ? 'Yes' : 'No'
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `screening_results_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  const sampleSymbols = [
    'AAPL, MSFT, GOOGL, AMZN, TSLA',
    'META, NFLX, NVDA, CRM, ADBE',
    'JPM, BAC, WFC, GS, MS',
    'JNJ, PFE, UNH, ABBV, MRK'
  ];

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        株式スクリーニング
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        複数の株式を条件に基づいて分析し、投資候補を見つけます。
      </Typography>

      {/* 入力フォーム */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            スクリーニング条件
          </Typography>
          
          <Box component="form" onSubmit={handleSubmit}>
            {/* 株式ティッカーシンボル */}
            <TextField
              fullWidth
              label="株式ティッカーシンボル（カンマ区切り）"
              variant="outlined"
              value={symbols}
              onChange={(e) => setSymbols(e.target.value)}
              placeholder="例: AAPL, MSFT, GOOGL, AMZN"
              helperText="複数の株式をカンマで区切って入力してください"
              sx={{ mb: 2 }}
              disabled={loading}
            />

            {/* サンプル株式 */}
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                サンプル株式（クリックして入力）：
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {sampleSymbols.map((symbolGroup, index) => (
                  <Chip
                    key={index}
                    label={symbolGroup}
                    variant="outlined"
                    size="small"
                    onClick={() => setSymbols(symbolGroup)}
                    sx={{ cursor: 'pointer' }}
                  />
                ))}
              </Box>
            </Box>

            <Divider sx={{ my: 2 }} />

            {/* フィルター条件 */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                フィルター条件（オプション）
              </Typography>
              <Button
                startIcon={<ClearIcon />}
                onClick={clearFilters}
                size="small"
                color="secondary"
              >
                クリア
              </Button>
            </Box>

            <Grid container spacing={2} sx={{ mb: 2 }}>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  fullWidth
                  label="最小時価総額"
                  type="number"
                  value={filters.minMarketCap}
                  onChange={handleFilterChange('minMarketCap')}
                  helperText="例: 1000000000 (10億)"
                  disabled={loading}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  fullWidth
                  label="最大PER"
                  type="number"
                  value={filters.maxPeRatio}
                  onChange={handleFilterChange('maxPeRatio')}
                  helperText="例: 25"
                  disabled={loading}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  fullWidth
                  label="最小ROE (%)"
                  type="number"
                  value={filters.minRoe}
                  onChange={handleFilterChange('minRoe')}
                  helperText="例: 15 (15%)"
                  disabled={loading}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  fullWidth
                  label="最大負債比率"
                  type="number"
                  value={filters.maxDebtToEquity}
                  onChange={handleFilterChange('maxDebtToEquity')}
                  helperText="例: 0.5"
                  disabled={loading}
                />
              </Grid>
              <Grid item xs={12} sm={6} md={4}>
                <TextField
                  fullWidth
                  label="最小流動比率"
                  type="number"
                  value={filters.minCurrentRatio}
                  onChange={handleFilterChange('minCurrentRatio')}
                  helperText="例: 1.5"
                  disabled={loading}
                />
              </Grid>
            </Grid>

            <Button
              type="submit"
              variant="contained"
              startIcon={loading ? <CircularProgress size={20} /> : <FilterListIcon />}
              disabled={loading}
              size="large"
            >
              {loading ? 'スクリーニング中...' : 'スクリーニング実行'}
            </Button>
          </Box>
        </CardContent>
      </Card>

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* 結果表示 */}
      {results && (
        <Card>
          <CardContent>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                スクリーニング結果
              </Typography>
              <Button
                startIcon={<DownloadIcon />}
                onClick={exportResults}
                variant="outlined"
                size="small"
              >
                CSV出力
              </Button>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary">
                分析対象: {results.total_symbols}銘柄 | 
                条件適合: {results.passed_symbols}銘柄 | 
                実行時間: {results.execution_time.toFixed(2)}秒
              </Typography>
            </Box>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>ティッカー</TableCell>
                    <TableCell>会社名</TableCell>
                    <TableCell align="right">スコア</TableCell>
                    <TableCell align="right">時価総額</TableCell>
                    <TableCell align="right">PER</TableCell>
                    <TableCell align="right">ROE</TableCell>
                    <TableCell align="right">負債比率</TableCell>
                    <TableCell align="right">流動比率</TableCell>
                    <TableCell align="center">適合</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {results.results.map((result: ScreeningResult) => (
                    <TableRow key={result.symbol}>
                      <TableCell>
                        <Typography variant="body2" fontWeight="bold">
                          {result.symbol}
                        </Typography>
                      </TableCell>
                      <TableCell>
                        <Typography variant="body2" noWrap>
                          {result.name}
                        </Typography>
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end' }}>
                          <Chip
                            icon={getScoreIcon(result.score)}
                            label={result.score.toFixed(1)}
                            color={getScoreColor(result.score)}
                            size="small"
                          />
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {formatCurrency(result.market_cap)}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(result.pe_ratio)}
                      </TableCell>
                      <TableCell align="right">
                        {formatPercentage(result.roe)}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(result.debt_to_equity)}
                      </TableCell>
                      <TableCell align="right">
                        {formatNumber(result.current_ratio)}
                      </TableCell>
                      <TableCell align="center">
                        <Chip
                          label={result.meets_criteria ? '適合' : '不適合'}
                          color={result.meets_criteria ? 'success' : 'default'}
                          size="small"
                        />
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}
    </Box>
  );
};

export default Screening;