# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a stock investment analysis project focused on identifying "low-risk, high-growth stocks" using quantitative and qualitative analysis methods. The project aims to develop tools and methodologies for stock screening and analysis.

## Current State

The repository is in early development stage with:
- Detailed analysis documentation in Japanese about risk-minimal stock analysis methods
- No code implementation yet
- Basic Claude configuration for permissions

## Key Concepts

The project centers around identifying stocks with these characteristics:
- Stable cash flow generation
- Low debt-to-equity ratios
- Strong brand power and market barriers
- Defensive business structures
- Appropriate valuation metrics (PER, PBR)
- Low volatility and beta values

## Data Sources Strategy

The project plans to use:
- **Yahoo Finance API** for quantitative financial data (cash flow, debt ratios, ROE/ROA, PER/PBR, beta values, trading volumes)
- **External sources** for qualitative analysis (corporate governance, ESG scores, industry reports, competitive analysis)

## Analysis Framework

The methodology involves:
1. **Primary screening** using Yahoo Finance API quantitative data
2. **Secondary analysis** using qualitative factors from external sources
3. **Cross-validation** using multiple data sources

## Development Guidelines

When implementing features:
- Focus on Japanese stock market analysis
- Implement both quantitative and qualitative analysis capabilities
- Consider data source reliability and freshness
- Build modular analysis components for different risk factors
- Plan for multi-source data integration

## Future Development Areas

Based on the analysis document, the system should eventually handle:
- Financial health scoring (debt ratios, cash ratios)
- Growth stability scoring (consistent revenue/profit growth)
- Valuation assessment (PER, PBR appropriateness)
- Risk indicators (beta, volatility)
- ESG and governance analysis
- Industry and competitive position analysis