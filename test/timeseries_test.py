from datetime import date
from tarfile import data_filter
import pandas as pd
import pytest
from src.models.timeseries import (
    DateOrderException,
    linear_timeseries,
    months_in_interval,
    Timeseries,
    DataToPeriodMismatch,
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
    with pytest.raises(DataToPeriodMismatch):
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


def test_timeseries_slicing(valid_monthly_timeseries):
    sliced_ts = valid_monthly_timeseries[date(2024, 2, 1) : date(2024, 4, 1)]
    assert sliced_ts.start_date == date(2024, 2, 1)
    assert sliced_ts.end_date == date(2024, 4, 1)
    assert len(sliced_ts.data) == 3


def test_timeseries_add(valid_monthly_timeseries):
    sliced_ts = valid_monthly_timeseries[date(2024, 2, 1) : date(2024, 4, 1)]
    added_ts = valid_monthly_timeseries + sliced_ts
    assert len(added_ts.data) == 12
    assert added_ts.data[0] == valid_monthly_timeseries.data[0]
    assert added_ts.data[2] == valid_monthly_timeseries.data[2] * 2


def test_timeseries_sub(valid_monthly_timeseries):
    sliced_ts = valid_monthly_timeseries[date(2024, 2, 1) : date(2024, 4, 1)]
    added_ts = valid_monthly_timeseries - sliced_ts
    assert len(added_ts.data) == 12
    assert added_ts.data[0] == valid_monthly_timeseries.data[0]
    assert added_ts.data[2] == 0


def test_timeseries_mul(valid_monthly_timeseries):
    sliced_ts = valid_monthly_timeseries[date(2024, 2, 1) : date(2024, 4, 1)]
    mul_ts = valid_monthly_timeseries * sliced_ts
    assert len(mul_ts.data) == 3
    assert mul_ts.data[0] == valid_monthly_timeseries.data[1] ** 2
    assert mul_ts.data[1] == valid_monthly_timeseries.data[2] ** 2
    assert mul_ts.data[2] == valid_monthly_timeseries.data[3] ** 2


def test_timeseries_div(valid_monthly_timeseries):
    sliced_ts = valid_monthly_timeseries[date(2024, 2, 1) : date(2024, 4, 1)]
    mul_ts = valid_monthly_timeseries / sliced_ts
    assert len(mul_ts.data) == 3
    assert mul_ts.data[0] == 1
    assert mul_ts.data[1] == 1
    assert mul_ts.data[2] == 1


def test_timeseries_index(valid_monthly_timeseries):
    sample = valid_monthly_timeseries[date(2024, 3, 1)]
    assert sample == valid_monthly_timeseries.data[2]


def test_linear_timeseries():
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    result = linear_timeseries(a=2, b=0, start=start_date, end=end_date)
    assert result.data == [2]*12
    result = linear_timeseries(a=2, b=1, start=start_date, end=end_date)
    assert result.data[0] == 2
    assert result.data[5] == 12
    assert result.data[11] == 24

