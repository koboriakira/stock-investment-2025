import React, { useState, useEffect } from 'react';
import {
  Box,
  TextField,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Chip,
  Divider,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from '@mui/material';
import {
  Search as SearchIcon,
  TrendingUp as TrendingUpIcon,
  TrendingDown as TrendingDownIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';

import { StockAPIService, formatCurrency, formatPercentage, formatNumber } from '../services/api';
import { StockInfo, FinancialScore } from '../types/stock';

const StockSearch: React.FC = () => {
  const [symbol, setSymbol] = useState<string>('');
  const [stockInfo, setStockInfo] = useState<StockInfo | null>(null);
  const [financialScore, setFinancialScore] = useState<FinancialScore | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symbol.trim()) {
      setError('株式ティッカーシンボルを入力してください');
      return;
    }

    setLoading(true);
    setError(null);
    setStockInfo(null);
    setFinancialScore(null);

    try {
      // 株式情報と財務スコアを並行して取得
      const [stockData, scoreData] = await Promise.all([
        StockAPIService.getStockInfo(symbol.trim().toUpperCase()),
        StockAPIService.getFinancialScore(symbol.trim().toUpperCase()).catch(() => null),
      ]);

      setStockInfo(stockData);
      setFinancialScore(scoreData);
    } catch (err) {
      setError(err instanceof Error ? err.message : '株式情報の取得に失敗しました');
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
    if (score >= 8) return <TrendingUpIcon />;
    if (score >= 6) return <ShowChartIcon />;
    return <TrendingDownIcon />;
  };

  const renderBasicInfo = () => {
    if (!stockInfo) return null;

    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h5" component="h2">
              {stockInfo.name} ({stockInfo.symbol})
            </Typography>
            <Typography variant="h4" color="primary">
              {formatCurrency(stockInfo.current_price)}
            </Typography>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">セクター</Typography>
              <Typography variant="body1">{stockInfo.sector || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">業界</Typography>
              <Typography variant="body1">{stockInfo.industry || 'N/A'}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">時価総額</Typography>
              <Typography variant="body1">{formatCurrency(stockInfo.market_cap)}</Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="body2" color="text.secondary">出来高</Typography>
              <Typography variant="body1">{stockInfo.volume?.toLocaleString() || 'N/A'}</Typography>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const renderFinancialScore = () => {
    if (!financialScore) return null;

    return (
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6" sx={{ mr: 2 }}>
              財務健全性スコア
            </Typography>
            <Chip
              icon={getScoreIcon(financialScore.overall_score)}
              label={`${financialScore.overall_score.toFixed(1)}/10`}
              color={getScoreColor(financialScore.overall_score)}
              variant="outlined"
            />
          </Box>
          
          <Grid container spacing={2}>
            {Object.entries(financialScore.detailed_scores).map(([key, value]) => (
              <Grid item xs={12} sm={6} md={4} key={key}>
                <Box sx={{ textAlign: 'center', p: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    {key === 'debt_score' && '負債スコア'}
                    {key === 'roe_score' && 'ROEスコア'}
                    {key === 'liquidity_score' && '流動性スコア'}
                    {key === 'pe_score' && 'PERスコア'}
                    {key === 'profit_score' && '利益率スコア'}
                  </Typography>
                  <Typography variant="h6" color={getScoreColor(value)}>
                    {value.toFixed(1)}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const renderFinancialMetrics = () => {
    if (!stockInfo) return null;

    const metrics = [
      { label: 'PER', value: formatNumber(stockInfo.pe_ratio) },
      { label: 'PBR', value: formatNumber(stockInfo.pb_ratio) },
      { label: 'PEG', value: formatNumber(stockInfo.peg_ratio) },
      { label: 'ROE', value: formatPercentage(stockInfo.roe) },
      { label: 'ROA', value: formatPercentage(stockInfo.roa) },
      { label: '負債比率', value: formatNumber(stockInfo.debt_to_equity) },
      { label: '流動比率', value: formatNumber(stockInfo.current_ratio) },
      { label: '当座比率', value: formatNumber(stockInfo.quick_ratio) },
      { label: '売上総利益率', value: formatPercentage(stockInfo.gross_margin) },
      { label: '営業利益率', value: formatPercentage(stockInfo.operating_margin) },
      { label: '純利益率', value: formatPercentage(stockInfo.profit_margin) },
      { label: '配当利回り', value: formatPercentage(stockInfo.dividend_yield) },
    ];

    return (
      <Card>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2 }}>
            主要財務指標
          </Typography>
          <TableContainer>
            <Table size="small">
              <TableHead>
                <TableRow>
                  <TableCell>指標</TableCell>
                  <TableCell align="right">値</TableCell>
                  <TableCell>指標</TableCell>
                  <TableCell align="right">値</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {Array.from({ length: Math.ceil(metrics.length / 2) }, (_, i) => {
                  const leftMetric = metrics[i * 2];
                  const rightMetric = metrics[i * 2 + 1];
                  return (
                    <TableRow key={i}>
                      <TableCell>{leftMetric.label}</TableCell>
                      <TableCell align="right">{leftMetric.value}</TableCell>
                      <TableCell>{rightMetric?.label || ''}</TableCell>
                      <TableCell align="right">{rightMetric?.value || ''}</TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    );
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        株式検索
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        株式のティッカーシンボル（例：AAPL、MSFT、GOOGL）を入力して、詳細な財務情報を取得します。
      </Typography>

      {/* 検索フォーム */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Box component="form" onSubmit={handleSearch} sx={{ display: 'flex', gap: 2 }}>
          <TextField
            fullWidth
            label="株式ティッカーシンボル"
            variant="outlined"
            value={symbol}
            onChange={(e) => setSymbol(e.target.value.toUpperCase())}
            placeholder="例: AAPL, MSFT, GOOGL"
            disabled={loading}
          />
          <Button
            type="submit"
            variant="contained"
            startIcon={loading ? <CircularProgress size={20} /> : <SearchIcon />}
            disabled={loading}
            sx={{ minWidth: 120 }}
          >
            {loading ? '検索中...' : '検索'}
          </Button>
        </Box>
      </Paper>

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {/* 検索結果 */}
      {stockInfo && (
        <Box>
          {renderBasicInfo()}
          {renderFinancialScore()}
          {renderFinancialMetrics()}
        </Box>
      )}
    </Box>
  );
};

export default StockSearch;