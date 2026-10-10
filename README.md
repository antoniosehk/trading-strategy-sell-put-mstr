# trading-strategy-sell-put-mstr

Systematic quantitative cash-secured short put selling strategy on **`US.MSTR`** (MicroStrategy Inc.) with a 200-day moving average trend filter, engineered for larger accounts ($50,000–$100,000+).

## Highlights
- **Macro Trend Filter (`MSTR Spot > SMA200`):** Enforces a strict 200-day simple moving average regime gatekeeper. Trading solely when MSTR trades above its 200-day SMA completely sidelines the strategy during prolonged bear regimes, avoiding the catastrophic drawdowns of the 2022 crypto winter.
- **Conservative Delta Selection (`delta_target: 0.16`):** Sells out-of-the-money puts at approximately 1 standard deviation OTM (~0.16 Delta). Given MSTR's extreme implied volatility (80%–130%), 0.16 Delta harvests substantial premium while providing an expansive margin of safety against aggressive equity pullbacks.
- **Tastytrade Mechanics:** Sells ~0.16 Delta Puts targeting 45 DTE on Fridays, systematically takes profit at 50% max credit, and rolls or closes trades at 21 DTE.
- **Defensive Adjustments:** Automated `ROLL_DOWN_AND_OUT` when tested (Spot ≤ Strike) or at 21 DTE to extend duration and improve breakevens.
- **Position Sizing & Capital Requirements:** Fixed 1 contract per entry (\$15,000–\$35,000 notional on \$100,000 capital) keeping cash collateral strictly ≤ 1.0× leverage (100% Cash-Secured).

## Specification
The canonical machine-readable specification is authored in [`STRATEGY.md`](./STRATEGY.md) with YAML frontmatter.

## Historical Performance Benchmark
Simulated across real historical ThetaData options data for `US.MSTR` from **2020-01-02** to **2026-09-30** (6.75 years):

| Metric | Result (Real ThetaData) |
| :--- | :--- |
| **Period** | `2020-01-02` to `2026-09-30` (6.75 Years) |
| **Initial Capital** | $100,000.00 |
| **Final NAV** | **$168,961.80** |
| **Total Return** | **+68.96%** ($+68,961.80) |
| **Annualized CAGR** | **+8.09%** |
| **Max Drawdown** | **-9.13%** (-$14,381.53) |
| **Sharpe Ratio** | 0.49 |
| **Sortino Ratio** | 0.64 |
| **Win Rate** | **84.4%** (119W / 22L, 141 positions) |
| **Profit Factor** | 1.60 |
| **Avg Win / Avg Loss** | $819.51 / -$2,770.16 |
| **Avg Days Held** | 12.4 days |
| **Total Trades Executed** | 283 |
| **Closed Positions** | 141 |
| **Total Commissions** | $183.95 |
| **Total Slippage** | $5,055.00 |
| **Cash Sweep Interest** | $32,394.75 |
| **Total Rolls** | 29 |
| **Data Source** | ThetaData v3 Real EOD Options & Parquet Lake |

_IV/Greeks: American (Bjerksund-Stensland 2002) with historical FRED Treasury rates and trailing dividends._

## Development & Testing
```bash
pytest --cov=trading_strategy_sell_put_mstr --cov-branch --cov-fail-under=100
```
