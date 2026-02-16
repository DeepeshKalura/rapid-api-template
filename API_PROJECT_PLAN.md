# 🌡️ Natural Gas Supply-Demand Analytics API

## 📋 EXECUTIVE SUMMARY

**Project Status**: Build Mode Active
**Based On**: EIA (U.S. Energy Information Administration) public domain data
**Template**: rapid-api-template (FastAPI + Python 3.12)
**Target Market**: Energy traders, commodity hedge funds, analysts
**Pricing**: $299-999/month vs competitors $10k+/year
**Timeline**: 2-3 months to MVP

---

## 🎯 VALUE PROPOSITION

### Problem It Solves
1. **Data Fragmentation**: Energy data scattered across EIA, production, storage, and imports reports
2. **Manual Correlation**: Traders manually calculate supply-demand spreads
3. **Historical Analysis**: Limited tools for backtesting seasonal patterns
4. **Enterprise Gatekeeping**: Competing solutions cost $10k+/year

### What We're NOT Building
❌ Futures price analytics (EIA futures data is stale - last update May 2024)
❌ Real-time trading signals
❌ LLM-based predictions (commodities traders don't trust AI forecasts)

### What We ARE Building
✅ **Supply-Demand Equilibrium API**: Correlate production, storage, consumption patterns
✅ **Seasonal Forecasting**: Historical seasonality patterns for supply indicators
✅ **Storage Analytics**: Underground storage capacity and utilization rates
✅ **Import/Export Flow**: Trade balance analytics by source/destination

---

## 📊 DATA STRATEGY (Based on EIA Research)

### ✅ AVAILABLE DATA (CURRENT)
| Data Type | Series ID | Date Range | Frequency | Update Frequency |
|-----------|-----------|------------|-----------|------------------|
| **Spot Price** | NG.RNGWHHD.M | 1997-01 to 2026-01 | Monthly | Current ✅ |
| **Storage Capacity** | NG.NGM_EPG0_SAD_R48_COUNT.M | 2013-01 to 2025-11 | Monthly | Current ✅ |
| **Production** | NG.NGM_EPG0_VG9_R3FM_MMCF.M | 2000-01 to 2024-12 | Monthly | 2024-12 (acceptable) |
| **Imports** | NG.NGM_EPG0_INC_NUS-MCA_MMCF.M | 2014-01 to 2025-11 | Monthly | Current ✅ |
| **Consumption** | NG.NA1570_*.M (by state) | 2010-01 to 2025-11 | Monthly | Current ✅ |

### ❌ UNAVAILABLE DATA
| Data Type | Issue | Workaround |
|-----------|-------|------------|
| **Monthly Futures Contracts** | Stale (last update May 2024) | Use historical futures for seasonality research only |
| **Real-time Prices** | Daily data limited (weekly only) | Focus on monthly analytics |
| **12-Month Forward Curve** | Only 4 generic contracts available | Build storage-driven forward curve predictions |

### 📦 Data Source
- **Primary**: EIA Bulk Download: https://www.eia.gov/opendata/bulk/NG.zip
- **License**: Public Domain (US government data)
- **Size**: ~4.5MB (17,947 series)
- **Update cadence**: Automatic downloads via GitHub Actions

---

## 🚀 API ENDPOINTS (MVP)

### 1. Supply Equilibrium Endpoints

#### `GET /supply/equilibrium`
Return supply-demand equilibrium analysis
```json
{
  "snapshot_date": "2026-01",
  "spot_price": 3.21,
  "storage_utilization": {
    "capacity_mcf": 4200000,
    "current_mcf": 3250000,
    "utilization_pct": 77.38
  },
  "production_index": 100.5,
  "import_export_balance": {
    "imports_mcf": 125000,
    "exports_mcf": 45000,
    "net_imports_mcf": 80000
  },
  "equilibrium_rating": "moderately_tight"
}
```

#### `GET /supply/seasonality?lookback=5y`
Historical seasonal patterns
```json
{
  "symbol": "NG",
  "lookback_years": 5,
  "seasonal_patterns": {
    "january": {"avg_price": 3.45, "avg_storage_util": 82.3},
    "february": {"avg_price": 3.12, "avg_storage_util": 78.5},
    "december": {"avg_price": 3.65, "avg_storage_util": 85.2}
  },
  "injection_season": {"start": "April", "end": "October"},
  "withdrawal_season": {"start": "November", "end": "March"}
}
```

### 2. Storage Analytics Endpoints

#### `GET /storage/levels`
Current storage vs 5-year average
```json
{
  "current_month": "2026-01",
  "current_storage_mcf": 3250000,
  "five_year_avg_mcf": 3100000,
  "deviation_pct": 4.84,
  "percentile": 68,
  "status": "above_average"
}
```

#### `GET /storage/capacity-by-region`
Underground storage capacity breakdown
```json
{
  "total_capacity_mcf": 4200000,
  "regions": [
    {"region": "East", "capacity_mcf": 1200000, "count": 15},
    {"region": "Midwest", "capacity_mcf": 950000, "count": 12},
    {"region": "South", "capacity_mcf": 1050000, "count": 8},
    {"region": "West", "capacity_mcf": 1000000, "count": 6}
  ]
}
```

### 3. Price Correlations Endpoints

#### `GET /prices/correlations`
Correlation between supply indicators and price
```json
{
  "timeframe": "5y",
  "correlations": [
    {"indicator": "storage_utilization", "correlation": -0.67, "significance": "high"},
    {"indicator": "production_index", "correlation": 0.42, "significance": "medium"},
    {"indicator": "net_imports", "correlation": 0.58, "significance": "high"}
  ],
  "recommended_leading_indicators": ["storage_utilization", "net_imports"]
}
```

#### `GET /prices/forward-curve-estimate`
Storage-driven forward curve estimate (12 months)
```json
{
  "base_date": "2026-01",
  "curve": [
    {"month": "2026-02", "estimated_price": 3.08, "confidence": 0.72},
    {"month": "2026-03", "estimated_price": 3.15, "confidence": 0.68},
    {"month": "2026-10", "estimated_price": 2.95, "confidence": 0.55}
  ],
  "methodology": "storage_utilization_regression"
}
```

### 4. Trade Flow Endpoints

#### `GET /trade/imports`
US natural gas imports breakdown
```json
{
  "month": "2026-01",
  "total_imports_mcf": 125000,
  "sources": [
    {"country": "Canada", "volume_mcf": 125000, "share_pct": 100.0, "avg_price_dollars": 3.45},
    {"country": "Mexico", "volume_mcf": 0, "share_pct": 0.0}
  ],
  "trend_vs_prev_month": "+2.3%"
}
```

#### `GET /trade/exports`
US natural gas exports by destination
```json
{
  "month": "2026-01",
  "total_exports_mcf": 45000,
  "destinations": [
    {"country": "Mexico", "volume_mcf": 30000, "share_pct": 66.7},
    {"country": "Canada", "volume_mcf": 10000, "share_pct": 22.2},
    {"country": "Other", "volume_mcf": 5000, "share_pct": 11.1}
  ]
}
```

### 5. Health & Metadata

#### `GET /ping`
Health check (per template)

#### `GET /meta/data-freshness`
Data update status
```json
{
  "last_bulk_download": "2026-02-15T10:30:00Z",
  "series_count": 17947,
  "key_series": [
    {"series_id": "NG.RNGWHHD.M", "last_update": "2026-02-04", "status": "current"},
    {"series_id": "NG.NGM_EPG0_SAD_R48_COUNT.M", "last_update": "2026-02-06", "status": "current"},
    {"series_id": "NG.RNGC1.M", "last_update": "2024-05-01", "status": "deprecated_futures"}
  ]
}
```

---

## 🛠 TECHNICAL ARCHITECTURE

### Project Structure
```
natural-gas-analytics/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic schemas
│   ├── services.py          # Data processing logic
│   ├── data_loader.py       # EIA data parsing
│   └── cache.py             # Redis caching
├── data/
│   ├── NG.zip               # EIA bulk download
│   └── processed/           # Processed data (postgres)
├── scripts/
│   ├── download_data.py     # CLI: Download EIA data
│   ├── init_db.py           # CLI: Initialize PostgreSQL
│   └── generate_openapi.py  # Auto-generate specs
├── tests/
│   ├── test_api.py
│   └── test_analytics.py
├── .github/workflows/
│   ├── data-update.yml      # Daily data downloads
│   └── ci.yml               # Tests + linting
├── Dockerfile
├── Dockerfile.prod
├── pyproject.toml
└── README.md
```

### Tech Stack
- **Framework**: FastAPI (from template)
- **Language**: Python 3.12 (from template)
- **Database**: PostgreSQL (time-series data)
- **Cache**: Redis (optional, for hot endpoints)
- **ETL**: uvicorn + requests
- **Validation**: Pydantic v2

### Dependencies (beyond template)
```toml
[project.dependencies]
requests = ">=2.31.0"
psycopg2-binary = ">=2.9.9"
pandas = ">=2.0.0"
numpy = ">=1.24.0"
scipy = ">=1.10.0"  # For seasonality calculations
```

---

## ⚠️ LIMITATIONS & STRATEGY

### Known Limitations
1. **No Real-time Futures**: EIA futures data is stale
   - **Mitigation**: Market ourselves as "supply-demand analytics", NOT "futures pricing"
   - **Differentiation**: We provide correlations that traders manually calculate

2. **Monthly Resolution**: No intraday data
   - **Mitigation**: Target swing traders and hedge funds (who use daily/weekly), NOT HFT firms
   - **Differentiation**: Focus on seasonal patterns (monthly is sufficient)

3. **US-Only Data**: No international gas markets
   - **Mitigation**: Niche market (US natural gas accounts for ~25% of global market)
   - **Expansion Path**: Add Europe/Asia data if MVP succeeds

4. **No Forward Curve Data**: Only 4 generic contracts
   - **Mitigation**: Build forward curve estimation using storage regression
   - **Differentiation**: Explain methodology clearly in docs (transparency builds trust)

### Go/No-Go Criteria
| Criterion | Threshold | Current Status | Decision |
|-----------|-----------|----------------|----------|
| Data Freshness | < 6 months old | ✅ Spot/Storage current, ⚠️ Futures stale | **GO** (exclude futures) |
| Historical Depth | 5+ years | ✅ 1994-2026 (30+ years) | **GO** |
| Market Size | $10k+/year opportunity | ✅ Existing $10k+ competitors | **GO** |
| Technical Complexity | Solo dev feasible | ✅ ETL + analytics | **GO** |

---

## 💰 PRICING STRATEGY

### Competitive Analysis
| Competitor | Price | Data | Target |
|------------|-------|------|--------|
| ICE Data Services | $10k+/year | Full futures, real-time | Hedge funds |
| Bloomberg Terminal | $24k+/year | Global, real-time | Banks |
| **Our API** | **$299-999/mo** | **US supply-demand analytics** | **Hedge funds, prop traders** |

### Pricing Tiers
- **Starter ($299/mo)**: 500 API calls/month, supply equilibrium endpoints only
- **Professional ($499/mo)**: 2,000 API calls/month, all endpoints + seasonality
- **Enterprise ($999/mo)**: 10,000 API calls/month, all endpoints + custom reports

### Revenue Projections
- **Month 1-3**: 0-2 customers ($0-1,998/mo)
- **Month 4-6**: 2-5 customers ($598-4,995/mo)
- **Month 7-12**: 5-15 customers ($1,495-14,985/mo)
- **Year 1 Target**: $30,000-50,000 ARR

---

## 📅 IMPLEMENTATION ROADMAP

### Phase 1: Core MVP (Week 1-4)
- [x] Data research and validation
- [ ] Repo setup from template
- [ ] EIA data ETL pipeline
- [ ] 3 core endpoints:
  - [ ] `GET /supply/equilibrium`
  - [ ] `GET /storage/levels`
  - [ ] `GET /prices/correlations`
- [ ] PostgreSQL schema
- [ ] Basic tests

### Phase 2: Advanced Analytics (Week 5-8)
- [ ] Additional endpoints:
  - [ ] `GET /supply/seasonality`
  - [ ] `GET /trade/imports`
  - [ ] `GET /trade/exports`
  - [ ] `GET /prices/forward-curve-estimate`
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Docker deployment
- [ ] OpenAPI spec generation

### Phase 3: Go-to-Market (Week 9-12)
- [ ] API documentation (with examples)
- [ ] Demo environment
- [ ] RapidAPI deployment
- [ ] Cold email outreach script
- [ ] Landing page (optional)

---

## 🎓 TARGET CUSTOMER ANALYSIS

### Primary Customers
1. **Prop Trading Firms** (70% of revenue)
   - Pain: Manual spreadsheet correlation of supply-demand indicators
   - Budget: $5k-20k/year for data
   - Decision makers: Head of analytics, portfolio manager

2. **Commodity Hedge Funds** (20% of revenue)
   - Pain: Lack of seasonal pattern tools for backtesting
   - Budget: $10k-50k/year for analytics
   - Decision makers: Quant researcher, portfolio manager

3. **Energy Analysts** (10% of revenue)
   - Pain: EIA data fragmented across reports
   - Budget: $2k-5k/year
   - Decision makers: Individual analysts, small firms

### Outbound Strategy
- **LinkedIn**: Search "Energy Analyst", "Commodity Trader", "Hedge Fund Manager"
- **Cold Email**: 20-30 emails/week, A/B test subject lines
- **Content**: "Why Your NG Forecast is Wrong" (storage correlation data)

---

## 🚀 GO-TO-MARKET CHECKLIST

### Pre-Launch (Week 1-4)
- [ ] Core 3 endpoints working
- [ ] API keys management (Rate limiting per tier)
- [ ] Payment gateway (Stripe for subscription management)
- [ ] Terms of service
- [ ] Privacy policy

### Launch (Week 5)
- [ ] RapidAPI listing
- [ ] Demo API account (free tier)
- [ ] LinkedIn profile optimization
- [ ] Cold email template

### Post-Launch (Week 6-12)
- [ ] Weekly outreach: 20-30 LinkedIn + cold emails
- [ ] User feedback collection
- [ ] Analytics dashboard (usage patterns)
- [ ] Feature prioritization based on demand

---

## 📈 SUCCESS METRICS

### KPIs (Key Performance Indicators)
1. **Revenue**: $30k ARR by month 12
2. **Active Subscribers**: 10+ paying customers by month 6
3. **API Response Time**: P95 < 200ms
4. **Data Freshness**: Always current (daily GitHub Actions)
5. **Customer Churn**: < 5% monthly

### Go/No-Go Triggers
- **Month 3**: If < 1 paying customer → pivot strategy
- **Month 6**: If < 5 paying customers → add features or pivot
- **Month 12**: If <$30k ARR → consider acquisition or shutdown

---

## 🔄 PIVOT PATHS (If MVP Fails)

### Pivot A: Add CME Futures Data (Cost: $500-2k/mo)
- **Trigger**: High demand for real-time futures
- **Action**: License CME Group API
- **Timeline**: +6 weeks integration
- **Pricing**: Increase tiers by $100-200/mo

### Pivot B: Expand to Commodities Portfolio
- **Trigger**: NG analytics successful, but limited market size
- **Action**: Add crude oil, heating oil, electricity
- **Timeline**: +3 months per commodity
- **Pricing**: Bundle deals (2+ commodities = 15% discount)

### Pivot C: ReeferLoad API (Already Validated)
- **Trigger**: NG analytics product-market fit mismatch
- **Action**: Switch to cold chain logistics API
- **Details**: See VALIDATED_IDEAS.md
- **Timeline**: 3-4 months from scratch

---

## 📞 CONTACT & SUPPORT

### Developer Contact
- **Email**: (to be added in .env.example)
- **GitHub Issues**: (repo URL)
- **Slack**: (to be added if team grows)

### API Support SLA
- **Starter/Professional**: 48-hour response
- **Enterprise**: 4-hour response, dedicated Slack channel

---

## ✅ READY TO BUILD

- [x] Data validation complete
- [x] Limitations documented
- [x] MVP endpoints defined
- [x] Tech stack finalized
- [x] Pricing strategy approved
- [ ] Repo initialization (in progress)
- [ ] ETL pipeline (pending)
- [ ] API implementation (pending)

**Status**: BUILD MODE ACTIVE
**Next Step**: Create private GitHub repo from template and implement Phase 1
