# trading-strategy-sell-put-mstr

Systematic quantitative cash-secured short put selling strategy on **`US.MSTR`** (MicroStrategy Inc.) with an **`IBIT`** (iShares Bitcoin Trust) macro 200-day moving average trend filter, engineered for larger accounts ($50,000–$100,000+).

## Highlights
- **Cross-Asset Macro Trend Filter:** Uses `IBIT` (spot Bitcoin ETF) 200-day SMA (`IBIT Spot > SMA200`) as the directional gatekeeper. Anchoring to physical spot Bitcoin filters out MicroStrategy's corporate convertible debt dilution, Net Asset Value (NAV) premium fluctuations, and excessive equity beta spikes.
- **Conservative Delta Selection (`delta_target: 0.16`):** Sells out-of-the-money puts at approximately 1 standard deviation OTM (~0.16 Delta). Given MSTR's extreme implied volatility (80%–130%), 0.16 Delta collects substantial premium while providing a wide margin of safety against aggressive daily drawdowns.
- **Tastytrade Mechanics:** Sells ~0.16 Delta Puts targeting 45 DTE on Fridays, systematically takes profit at 50% max credit, and rolls or closes trades at 21 DTE.
- **Defensive Adjustments:** Automated `ROLL_DOWN_AND_OUT` when tested ($\text{Spot} \le \text{Strike}$) or at 21 DTE to extend duration and improve breakevens.
- **Position Sizing & Capital Requirements:** Fixed 1 contract per entry ($15,000–$35,000 notional on $100,000 capital) keeping cash collateral strictly $\le 1.0\times$ leverage (100% Cash-Secured).

## Specification
The canonical machine-readable specification is authored in [`STRATEGY.md`](./STRATEGY.md) with YAML frontmatter.

## Historical Performance Benchmark
Simulated across real historical ThetaData options data for `US.MSTR` and underlying `IBIT` from **2024-11-20** to **2026-09-30** (1.86 years):

| Metric | Result (Real ThetaData) |
| :--- | :--- |
| **Period** | `2024-11-20` to `2026-09-30` (1.86 Years) |
| **Initial Capital** | $100,000.00 |
| **Final NAV** | $115,786.00 |
| **Total Return** | **+15.79%** ($+15,786.00) |
| **Annualized CAGR** | **+8.20%** |
| **Max Drawdown** | **-5.55%** (-$5,989.28) |
| **Sharpe Ratio** | 0.54 |
| **Sortino Ratio** | 0.76 |
| **Win Rate** | **81.1%** (43W / 10L, 53 positions) |
| **Profit Factor** | 1.66 |
| **Avg Win / Avg Loss** | $494.72 / -$1,278.40 |
| **Avg Days Held** | 12.0 days |
| **Total Trades Executed** | 107 |
| **Closed Positions** | 53 |
| **Total Commissions** | $69.55 |
| **Total Slippage** | $763.00 |
| **Cash Sweep Interest** | $7,307.55 |
| **Total Rolls** | 16 |
| **Data Source** | ThetaData v3 Real EOD Options & Parquet Lake |

_IV/Greeks: American (Bjerksund-Stensland 2002) with historical FRED Treasury rates and trailing dividends._

## Development & Testing
```bash
pytest --cov=trading_strategy_sell_put_mstr --cov-branch --cov-fail-under=100
```
