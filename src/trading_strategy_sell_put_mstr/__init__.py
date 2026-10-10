"""
trading-strategy-sell-put-mstr

Tastytrade mechanics for selling out-of-the-money cash-secured puts on US.MSTR
with IBIT macro 200-day trend filter.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from trading_strategy_core.models import StrategySpec
from trading_strategy_core.parser import StrategyParser

STRATEGY_PATH = Path(__file__).resolve().parent.parent.parent / "STRATEGY.md"


def load_strategy(path: Optional[Path | str] = None) -> StrategySpec:
    """Loads and validates the StrategySpec from STRATEGY.md."""
    target_path = Path(path) if path is not None else STRATEGY_PATH
    if not target_path.exists():
        raise FileNotFoundError(f"Strategy file not found at {target_path}")

    spec = StrategyParser().parse_file(str(target_path))
    validate_strategy(spec)
    return spec


def validate_strategy(spec: StrategySpec) -> bool:
    """Validates that a StrategySpec strictly meets the Short Put specification."""
    if spec.name != "trading-strategy-sell-put-mstr":
        raise ValueError(
            f"Strategy name must be 'trading-strategy-sell-put-mstr', got '{spec.name}'"
        )
    if spec.underlying != "US.MSTR":
        raise ValueError(f"Underlying must be 'US.MSTR', got '{spec.underlying}'")
    if spec.strategy_type != "SHORT_PUT":
        raise ValueError(f"Strategy type must be 'SHORT_PUT', got '{spec.strategy_type}'")
    if spec.entry_rules is None:
        raise ValueError("Entry rules must be defined")
    if spec.exit_rules is None:
        raise ValueError("Exit rules must be defined")

    if spec.entry_rules.default_contracts <= 0:
        raise ValueError("Default contracts must be positive")

    if spec.entry_rules.dte_target <= 0:
        raise ValueError("DTE target must be positive")

    if spec.entry_rules.min_ivr < 0:
        raise ValueError("Min IVR cannot be negative")

    if (
        spec.exit_rules.profit_target_pct is None
        or not (0.0 < spec.exit_rules.profit_target_pct < 1.0)
    ):
        raise ValueError("Profit target percentage must be between 0.0 and 1.0")

    return True


def calculate_collateral(strike: float, contracts: int = 1) -> float:
    """
    Calculates cash collateral required to secure a short put position:
    Collateral = Strike * 100 * contracts
    """
    if strike <= 0:
        raise ValueError("Strike must be a positive number")
    if contracts <= 0:
        raise ValueError("Contracts must be a positive integer")

    return round(strike * 100.0 * contracts, 2)


def calculate_max_profit(premium: float, contracts: int = 1) -> float:
    """Calculates maximum dollar profit for a cash-secured put."""
    if premium <= 0:
        raise ValueError("Premium must be a positive number")
    if contracts <= 0:
        raise ValueError("Contracts must be a positive integer")

    return round(premium * 100.0 * contracts, 2)


def calculate_max_loss(strike: float, premium: float, contracts: int = 1) -> float:
    """
    Calculates maximum dollar loss (down to $0 underlying price):
    Max Loss = (Strike - Premium) * 100 * contracts
    """
    if strike <= 0:
        raise ValueError("Strike must be a positive number")
    if premium <= 0:
        raise ValueError("Premium must be a positive number")
    if contracts <= 0:
        raise ValueError("Contracts must be a positive integer")
    if premium >= strike:
        raise ValueError("Premium cannot equal or exceed strike price")

    return round((strike - premium) * 100.0 * contracts, 2)


def calculate_breakeven(strike: float, premium: float) -> float:
    """
    Calculates expiration breakeven price:
    Breakeven = Strike - Premium
    """
    if strike <= 0:
        raise ValueError("Strike must be a positive number")
    if premium <= 0:
        raise ValueError("Premium must be a positive number")

    return round(strike - premium, 2)


def calculate_return_on_capital(premium: float, strike: float) -> float:
    """
    Calculates the unannualized return on capital (ROC):
    ROC = Premium / Strike
    """
    if premium <= 0:
        raise ValueError("Premium must be a positive number")
    if strike <= 0:
        raise ValueError("Strike must be a positive number")

    return round(premium / strike, 4)
