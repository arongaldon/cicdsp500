# test_sp500.py
"""Unit tests on sp500.py."""

import pandas as pd
import pytest
from sp500 import InvestmentCalculator

fake_hist = pd.DataFrame({ 'Date': [f'2023-{month:02d}-01' for month in range(1, 13)]
                           .append([f'2024-{month:02d}-01' for month in range(1, 13)])
                         , 'Close': [float(x) for x in range(100, 340, 10)] })

@pytest.fixture(name="get_sp500_data")
def fixture_get_sp500_data(mocker):
    """Mock S&P 500 historical data"""
    return mocker.patch("sp500.InvestmentCalculator.get_sp500_data")

def test_calculate_contributed(get_sp500_data) -> None:
    """Test with empty data (no historical prices)"""
    get_sp500_data.return_value = pd.DataFrame()

    initial = 10000.0
    monthly = 500.0
    years = 5
    calculator = InvestmentCalculator(initial, monthly, years)
    result = calculator.calculate_contributed()

    expected_contribution = initial + monthly * 12 * years
    assert result == expected_contribution

def test_calculate_total(get_sp500_data) -> None:
    """Test with mock data (sample historical prices)"""
    get_sp500_data.return_value = fake_hist

    initial = 10000.0
    monthly = 500.0
    years = 1
    calculator = InvestmentCalculator(initial, monthly, years)
    result = calculator.calculate_total()

    expected_shares = 262280.00
    assert result == pytest.approx(expected_shares, 1e-5)

def test_calculate_total_empty_data(get_sp500_data) -> None:
    """Test with empty data (no historical prices)"""
    get_sp500_data.return_value = pd.DataFrame()

    initial = 10000.0
    monthly = 500.0
    years = 1
    calculator = InvestmentCalculator(initial, monthly, years)
    result = calculator.calculate_total()

    assert result == 0.0
