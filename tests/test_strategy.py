"""
Unit tests for trading-strategy-sell-put-mstr.
"""

from copy import deepcopy
from pathlib import Path
import pytest

from trading_strategy_core.models import StrategySpec
from trading_strategy_sell_put_mstr import (
    STRATEGY_PATH,
    calculate_breakeven,
    calculate_collateral,
    calculate_max_loss,
    calculate_max_profit,
    calculate_return_on_capital,
    load_strategy,
    validate_strategy,
)


def test_load_strategy_success():
    spec = load_strategy()
    assert spec.name == "trading-strategy-sell-put-mstr"
    assert spec.version == "1.0.1"
    assert spec.enabled is True
    assert spec.underlying == "US.MSTR"
    assert spec.strategy_type == "SHORT_PUT"
    assert spec.entry_rules.default_contracts == 1
    assert spec.entry_rules.max_active_positions == 2
    assert spec.entry_rules.min_ivr == 0.0
    assert spec.entry_rules.dte_target == 45
    assert spec.entry_rules.delta_target == 0.16
    assert spec.entry_rules.trend_filter is not None
    assert spec.entry_rules.trend_filter.enabled is True
    assert spec.entry_rules.trend_filter.underlying == "MSTR"
    assert spec.exit_rules.profit_target_pct == 0.50
    assert spec.exit_rules.time_stop_dte == 21


def test_load_strategy_custom_path():
    spec = load_strategy(str(STRATEGY_PATH))
    assert spec.name == "trading-strategy-sell-put-mstr"


def test_load_strategy_file_not_found():
    with pytest.raises(FileNotFoundError, match="Strategy file not found"):
        load_strategy("non_existent_file.md")


def test_validate_strategy_mutations():
    valid_spec = load_strategy()

    # Invalid name
    bad_name = deepcopy(valid_spec)
    bad_name.name = "wrong-name"
    with pytest.raises(ValueError, match="Strategy name must be"):
        validate_strategy(bad_name)

    # Invalid underlying
    bad_und = deepcopy(valid_spec)
    bad_und.underlying = "US.SPY"
    with pytest.raises(ValueError, match="Underlying must be 'US.MSTR'"):
        validate_strategy(bad_und)

    # Invalid strategy_type
    bad_type = deepcopy(valid_spec)
    bad_type.strategy_type = "BULL_PUT_SPREAD"
    with pytest.raises(ValueError, match="Strategy type must be 'SHORT_PUT'"):
        validate_strategy(bad_type)

    # Missing entry_rules
    bad_entry = deepcopy(valid_spec)
    bad_entry.entry_rules = None  # type: ignore[assignment]
    with pytest.raises(ValueError, match="Entry rules must be defined"):
        validate_strategy(bad_entry)

    # Missing exit_rules
    bad_exit = deepcopy(valid_spec)
    bad_exit.exit_rules = None  # type: ignore[assignment]
    with pytest.raises(ValueError, match="Exit rules must be defined"):
        validate_strategy(bad_exit)

    # Default contracts invalid
    bad_qty = deepcopy(valid_spec)
    bad_qty.entry_rules.default_contracts = 0
    with pytest.raises(ValueError, match="Default contracts must be positive"):
        validate_strategy(bad_qty)

    # DTE target invalid
    bad_dte = deepcopy(valid_spec)
    bad_dte.entry_rules.dte_target = 0
    with pytest.raises(ValueError, match="DTE target must be positive"):
        validate_strategy(bad_dte)

    # Min IVR invalid
    bad_ivr = deepcopy(valid_spec)
    bad_ivr.entry_rules.min_ivr = -1.0
    with pytest.raises(ValueError, match="Min IVR cannot be negative"):
        validate_strategy(bad_ivr)

    # Profit target invalid
    bad_pt_none = deepcopy(valid_spec)
    bad_pt_none.exit_rules.profit_target_pct = None
    with pytest.raises(ValueError, match="Profit target percentage must be between 0.0 and 1.0"):
        validate_strategy(bad_pt_none)

    bad_pt_high = deepcopy(valid_spec)
    bad_pt_high.exit_rules.profit_target_pct = 1.0
    with pytest.raises(ValueError, match="Profit target percentage must be between 0.0 and 1.0"):
        validate_strategy(bad_pt_high)


def test_calculate_collateral():
    assert calculate_collateral(150.0, 1) == 15000.0
    assert calculate_collateral(150.0, 2) == 30000.0

    with pytest.raises(ValueError, match="Strike must be a positive number"):
        calculate_collateral(-1.0)

    with pytest.raises(ValueError, match="Contracts must be a positive integer"):
        calculate_collateral(150.0, 0)


def test_calculate_max_profit():
    assert calculate_max_profit(5.0, 1) == 500.0
    assert calculate_max_profit(5.0, 2) == 1000.0

    with pytest.raises(ValueError, match="Premium must be a positive number"):
        calculate_max_profit(0.0)

    with pytest.raises(ValueError, match="Contracts must be a positive integer"):
        calculate_max_profit(1.0, -1)


def test_calculate_max_loss():
    assert calculate_max_loss(150.0, 5.0, 1) == 14500.0
    assert calculate_max_loss(150.0, 5.0, 2) == 29000.0

    with pytest.raises(ValueError, match="Strike must be a positive number"):
        calculate_max_loss(0.0, 1.0)

    with pytest.raises(ValueError, match="Premium must be a positive number"):
        calculate_max_loss(150.0, -1.0)

    with pytest.raises(ValueError, match="Contracts must be a positive integer"):
        calculate_max_loss(150.0, 1.0, 0)

    with pytest.raises(ValueError, match="Premium cannot equal or exceed strike price"):
        calculate_max_loss(150.0, 150.0)


def test_calculate_breakeven():
    assert calculate_breakeven(150.0, 5.0) == 145.0

    with pytest.raises(ValueError, match="Strike must be a positive number"):
        calculate_breakeven(-10.0, 1.0)

    with pytest.raises(ValueError, match="Premium must be a positive number"):
        calculate_breakeven(150.0, 0.0)


def test_calculate_return_on_capital():
    assert calculate_return_on_capital(5.0, 150.0) == 0.0333

    with pytest.raises(ValueError, match="Premium must be a positive number"):
        calculate_return_on_capital(-1.0, 150.0)

    with pytest.raises(ValueError, match="Strike must be a positive number"):
        calculate_return_on_capital(5.0, -150.0)
