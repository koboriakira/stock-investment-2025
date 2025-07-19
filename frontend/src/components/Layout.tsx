import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  Container,
  Paper,
  Breadcrumbs,
  Link as MuiLink,
} from '@mui/material';
import {
  Dashboard as DashboardIcon,
  Search as SearchIcon,
  FilterList as FilterListIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation();

  const navigationItems = [
    { path: '/', label: 'ダッシュボード', icon: <DashboardIcon /> },
    { path: '/search', label: '株式検索', icon: <SearchIcon /> },
    { path: '/screening', label: 'スクリーニング', icon: <FilterListIcon /> },
  ];

  const getBreadcrumbs = () => {
    const pathnames = location.pathname.split('/').filter((x) => x);
    
    const breadcrumbNameMap: { [key: string]: string } = {
      '/': 'ダッシュボード',
      '/search': '株式検索',
      '/screening': 'スクリーニング',
    };

    return (
      <Breadcrumbs aria-label="breadcrumb">
        <MuiLink
          component={Link}
          to="/"
          color="inherit"
          underline="hover"
          sx={{ display: 'flex', alignItems: 'center' }}
        >
          <DashboardIcon sx={{ mr: 0.5 }} fontSize="inherit" />
          ホーム
        </MuiLink>
        {pathnames.map((_, index) => {
          const routeTo = `/${pathnames.slice(0, index + 1).join('/')}`;
          const isLast = index === pathnames.length - 1;
          
          return isLast ? (
            <Typography key={routeTo} color="text.primary">
              {breadcrumbNameMap[routeTo]}
            </Typography>
          ) : (
            <MuiLink
              key={routeTo}
              component={Link}
              to={routeTo}
              color="inherit"
              underline="hover"
            >
              {breadcrumbNameMap[routeTo]}
            </MuiLink>
          );
        })}
      </Breadcrumbs>
    );
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      {/* ヘッダー */}
      <AppBar position="static" elevation={0}>
        <Toolbar>
          <TrendingUpIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            StockScreener
          </Typography>
          
          {/* ナビゲーションメニュー */}
          <Box sx={{ display: 'flex', gap: 1 }}>
            {navigationItems.map((item) => (
              <Button
                key={item.path}
                color="inherit"
                component={Link}
                to={item.path}
                startIcon={item.icon}
                sx={{
                  backgroundColor: location.pathname === item.path ? 'rgba(255, 255, 255, 0.1)' : 'transparent',
                  '&:hover': {
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                  },
                }}
              >
                {item.label}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </AppBar>

      {/* メインコンテンツ */}
      <Container maxWidth="xl" sx={{ mt: 2, mb: 4 }}>
        {/* パンくずリスト */}
        <Box sx={{ mb: 2 }}>
          {getBreadcrumbs()}
        </Box>

        {/* コンテンツエリア */}
        <Paper elevation={1} sx={{ p: 3, minHeight: '70vh' }}>
          {children}
        </Paper>
      </Container>

      {/* フッター */}
      <Box
        component="footer"
        sx={{
          py: 2,
          px: 3,
          mt: 'auto',
          backgroundColor: 'background.paper',
          borderTop: 1,
          borderColor: 'divider',
        }}
      >
        <Container maxWidth="xl">
          <Typography variant="body2" color="text.secondary" align="center">
            © 2025 StockScreener. 本ツールは教育・研究目的で作成されており、投資助言を提供するものではありません。
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Layout;