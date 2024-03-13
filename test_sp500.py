# test_sp500.py

import pandas as pd
import pytest, pytest_mock
from sp500 import calculate_result

fake_hist = pd.DataFrame({ 'Date': [f'2023-{month:02d}-01' for month in range(1, 13)].append([f'2024-{month:02d}-01' for month in range(1, 13)])
                         , 'Close': [float(x) for x in range(4000, 6400, 100)] })

@pytest.fixture
def mock_get_sp500_data(mocker):
    """Mock S&P 500 historical data"""
    return mocker.patch("sp500.get_sp500_data")

def test_calculate_result(mock_get_sp500_data) -> None:
    """Test with mock data (sample historical prices)"""

    mock_get_sp500_data.return_value = fake_hist

    initial = 10000.0
    monthly = 500.0
    years = 1
    result = calculate_result(initial, monthly, years)

    expected_shares = (initial + (monthly * 12)) / 4000.0
    assert result == expected_shares * 4000.0

def test_calculate_result_empty_data(mock_get_sp500_data) -> None:
    """Test with empty data (no historical prices)"""
    
    mock_get_sp500_data.return_value = pd.DataFrame()

    initial = 10000.0
    monthly = 500.0
    years = 1
    result = calculate_result(initial, monthly, years)
    assert result == 0.0
