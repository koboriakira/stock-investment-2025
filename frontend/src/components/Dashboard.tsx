import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Alert,
  CircularProgress,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@mui/material';
import {
  Search as SearchIcon,
  FilterList as FilterListIcon,
  TrendingUp as TrendingUpIcon,
  ShowChart as ShowChartIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { Link } from 'react-router-dom';

import { StockAPIService } from '../services/api';

const Dashboard: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [systemInfo, setSystemInfo] = useState<any>(null);

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const result = await StockAPIService.healthCheck();
      setApiStatus('online');
      setSystemInfo(result);
    } catch (error) {
      setApiStatus('offline');
      console.error('API health check failed:', error);
    }
  };

  const getStatusIcon = () => {
    switch (apiStatus) {
      case 'checking':
        return <CircularProgress size={20} />;
      case 'online':
        return <CheckCircleIcon color="success" />;
      case 'offline':
        return <ErrorIcon color="error" />;
      default:
        return <WarningIcon color="warning" />;
    }
  };

  const getStatusText = () => {
    switch (apiStatus) {
      case 'checking':
        return 'システム状態確認中...';
      case 'online':
        return 'システム正常動作中';
      case 'offline':
        return 'システムに接続できません';
      default:
        return '不明な状態';
    }
  };

  const features = [
    {
      title: '株式検索',
      description: '個別株式の詳細な財務情報と分析を取得',
      icon: <SearchIcon />,
      link: '/search',
      color: 'primary',
    },
    {
      title: 'スクリーニング',
      description: '複数の株式を条件に基づいて一括分析',
      icon: <FilterListIcon />,
      link: '/screening',
      color: 'secondary',
    },
  ];

  const analysisFeatures = [
    '財務健全性スコア算出',
    '主要財務指標の分析',
    'リスク評価（ベータ値、ボラティリティ）',
    'バリュエーション分析（PER、PBR、PEG）',
    '収益性分析（ROE、ROA、利益率）',
    '流動性分析（流動比率、当座比率）',
    '成長性分析（売上・利益成長率）',
  ];

  const sampleSymbols = [
    { symbol: 'AAPL', name: 'Apple Inc.' },
    { symbol: 'MSFT', name: 'Microsoft Corporation' },
    { symbol: 'GOOGL', name: 'Alphabet Inc.' },
    { symbol: 'AMZN', name: 'Amazon.com Inc.' },
    { symbol: 'TSLA', name: 'Tesla Inc.' },
    { symbol: 'NVDA', name: 'NVIDIA Corporation' },
    { symbol: 'META', name: 'Meta Platforms Inc.' },
    { symbol: 'NFLX', name: 'Netflix Inc.' },
  ];

  return (
    <Box>
      <Typography variant="h3" component="h1" gutterBottom>
        StockScreener
      </Typography>
      
      <Typography variant="h6" color="text.secondary" paragraph>
        Yahoo Finance APIを活用した株式分析・スクリーニングツール
      </Typography>

      {/* システム状態 */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            {getStatusIcon()}
            <Typography variant="h6" sx={{ ml: 1 }}>
              システム状態
            </Typography>
          </Box>
          <Typography variant="body1" color={apiStatus === 'online' ? 'success.main' : 'error.main'}>
            {getStatusText()}
          </Typography>
          {systemInfo && (
            <Box sx={{ mt: 1 }}>
              <Typography variant="body2" color="text.secondary">
                API: {systemInfo.api} | Status: {systemInfo.status}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      {/* 機能カード */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {features.map((feature) => (
          <Grid item xs={12} md={6} key={feature.title}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  {feature.icon}
                  <Typography variant="h5" sx={{ ml: 1 }}>
                    {feature.title}
                  </Typography>
                </Box>
                <Typography variant="body1" color="text.secondary" paragraph>
                  {feature.description}
                </Typography>
                <Button
                  component={Link}
                  to={feature.link}
                  variant="contained"
                  color={feature.color as 'primary' | 'secondary'}
                  fullWidth
                >
                  {feature.title}を開始
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Grid container spacing={3}>
        {/* 分析機能一覧 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <ShowChartIcon sx={{ mr: 1 }} />
                分析機能
              </Typography>
              <List dense>
                {analysisFeatures.map((feature, index) => (
                  <ListItem key={index} sx={{ pl: 0 }}>
                    <ListItemIcon>
                      <TrendingUpIcon color="primary" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText primary={feature} />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* サンプル株式 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <InfoIcon sx={{ mr: 1 }} />
                サンプル株式
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                以下の株式で機能をお試しください：
              </Typography>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {sampleSymbols.map((stock) => (
                  <Chip
                    key={stock.symbol}
                    label={stock.symbol}
                    variant="outlined"
                    size="small"
                    component={Link}
                    to={`/search?symbol=${stock.symbol}`}
                    sx={{
                      textDecoration: 'none',
                      '&:hover': {
                        backgroundColor: 'primary.light',
                        color: 'white',
                      },
                    }}
                  />
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 免責事項 */}
      <Alert severity="info" sx={{ mt: 3 }}>
        <Typography variant="body2">
          <strong>免責事項:</strong> 
          本ツールは教育・研究目的で作成されており、投資助言を提供するものではありません。
          投資判断は自己責任で行ってください。Yahoo Finance APIから取得したデータの正確性について保証するものではありません。
        </Typography>
      </Alert>
    </Box>
  );
};

export default Dashboard;