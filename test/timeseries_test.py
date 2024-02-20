from datetime import date
import pandas as pd
import pytest
from src.models.timeseries import (
    DateOrderException,
    Timeseries,
    DataToPeriodMissmatch,
    constant_timeseries,
)


@pytest.fixture
def valid_monthly_timeseries():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    data = range(12)
    return Timeseries(start_date=start_date, end_date=end_date, data=data)


@pytest.fixture
def invalid_timeseries_mismatched_data():
    start_date = date(2021, 12, 1)
    end_date = date(2024, 2, 1)
    data = [1, 2, 3, 4]
    return start_date, end_date, data


@pytest.fixture
def invalid_timeseries_mismatched_date_order():
    start_date = date(2024, 12, 1)
    end_date = date(2023, 1, 31)
    data = [1, 2, 3, 4]
    return start_date, end_date, data


def test_valid_monthly_timeseries(valid_monthly_timeseries):
    assert len(valid_monthly_timeseries.data) == 12


def test_invalid_timeseries_mismatched_data(invalid_timeseries_mismatched_data):
    start_date, end_date, data = invalid_timeseries_mismatched_data
    with pytest.raises(DataToPeriodMissmatch):
        Timeseries(start_date=start_date, end_date=end_date, data=data)


def test_invalid_timeseries_mismatched_date_order(
    invalid_timeseries_mismatched_date_order,
):
    start_date, end_date, data = invalid_timeseries_mismatched_date_order
    with pytest.raises(DateOrderException):
        Timeseries(start_date=start_date, end_date=end_date, data=data)


def test_constant_timeseries():
    ts = constant_timeseries(100, date(2022, 1, 1), date(2022, 12, 31))
    assert ts.start_date == date(2022, 1, 1)
    assert ts.end_date == date(2022, 12, 31)
    assert len(ts.data) == 12
    assert all(value == 100 for value in ts.data)
