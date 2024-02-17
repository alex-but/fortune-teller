from datetime import date
import pandas as pd
import pytest
from src.models.timeseries import (
    DateOrderException,
    Period,
    Timeseries,
    DataToPeriodMissmatch,
)


@pytest.fixture
def valid_daily_timeseries():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    period = Period.Daily
    data = range(31)
    return Timeseries(
        start_date=start_date, end_date=end_date, period=period, data=data
    )


@pytest.fixture
def valid_monthly_timeseries():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    period = Period.Monthly
    data = range(12)
    return Timeseries(
        start_date=start_date, end_date=end_date, period=period, data=data
    )


@pytest.fixture
def invalid_timeseries_mismatched_data():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 1, 31)
    period = Period.Daily
    data = [1, 2, 3, 4]
    return start_date, end_date, period, data


@pytest.fixture
def invalid_timeseries_mismatched_date_order():
    start_date = date(2024, 1, 1)
    end_date = date(2023, 1, 31)
    period = Period.Daily
    data = [1, 2, 3, 4]
    return start_date, end_date, period, data


def test_valid_daily_timeseries(valid_daily_timeseries):
    assert len(valid_daily_timeseries.pd_timeseries) == 31


def test_valid_monthly_timeseries(valid_monthly_timeseries):
    assert len(valid_monthly_timeseries.pd_timeseries) == 12


def test_invalid_timeseries_mismatched_data(invalid_timeseries_mismatched_data):
    start_date, end_date, period, data = invalid_timeseries_mismatched_data
    with pytest.raises(DataToPeriodMissmatch):
        Timeseries(start_date=start_date, end_date=end_date, period=period, data=data)


def test_invalid_timeseries_mismatched_date_order(
    invalid_timeseries_mismatched_date_order,
):
    start_date, end_date, period, data = invalid_timeseries_mismatched_date_order
    with pytest.raises(DateOrderException):
        Timeseries(start_date=start_date, end_date=end_date, period=period, data=data)
