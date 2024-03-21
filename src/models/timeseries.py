"""Module for handling timeseries of data
"""

from dataclasses import dataclass
from datetime import date

import pandas as pd


def months_in_interval(start: date, end: date) -> int:
    """returns the number of months in a date interval"""
    return (end.year - start.year) * 12 + end.month - start.month + 1


class DateOrderException(Exception):
    """End date is before the beginning date"""

    def __init__(self, start_date: date, end_date: date, message: str):
        self.start_date = start_date
        self.end_date = end_date
        self.message = message
        super().__init__(message)


class IncludePeriodMismatch(Exception):
    """Error raised when a period have to be included in another period"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class DataToPeriodMismatch(Exception):
    """Show that data does not have the number of samples expected by a timeseries"""

    def __init__(
        self,
        start_date: date,
        end_date: date,
        no_samples: int,
        message: str,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.no_samples = no_samples
        self.message = message
        super().__init__(message)


def get_slice_indexes_from_date_intervals(base: slice, contained: slice) -> slice:

    if (
        not base.start <= contained.start < base.stop
        or not base.start < contained.stop <= base.stop
    ):
        raise IncludePeriodMismatch(
            message=f"""slice period {contained.start}->{contained.stop} is not included in timeseries period {base.start} -> {base.stop}""",
        )
    # Calculate the index corresponding to the start date
    start_index = months_in_interval(base.start, contained.start) - 1

    # Calculate the index corresponding to the end date
    end_index = months_in_interval(base.start, contained.stop)

    return slice(start_index, end_index)


@dataclass(kw_only=True)
class Timeseries:
    """A timeseries of Monthly data."""

    start_date: date
    end_date: date
    data: list[float]

    def __post_init__(self):
        if self.start_date > self.end_date:
            raise DateOrderException(
                start_date=self.start_date,
                end_date=self.end_date,
                message=f"""start date {self.start_date} is later than
                            end date {self.end_date} in the timeseries""",
            )

        if months_in_interval(self.start_date, self.end_date) != len(self.data):
            raise DataToPeriodMismatch(
                start_date=self.start_date,
                end_date=self.end_date,
                no_samples=len(self.data),
                message=f"""Timeseries init error: The length of the data {len(self.data)} does not match the number of samples from the period: {months_in_interval(self.start_date, self.end_date)}""",
            )

    def __add__(self, other):
        """addition operation will add data matching the same time indexes and
        fill the difference with zeros.
        """
        # Implementation details for addition operation...
        add_start_date = min(self.start_date, other.end_date)
        add_end_date = max(self.end_date, other.end_date)
        added_timeseries = Timeseries(
            start_date=add_start_date,
            end_date=add_end_date,
            data=[0] * months_in_interval(add_start_date, add_end_date),
        )
        self_slice_interval = get_slice_indexes_from_date_intervals(
            slice(add_start_date, add_end_date), slice(self.start_date, self.end_date)
        )
        other_slice_interval = get_slice_indexes_from_date_intervals(
            slice(add_start_date, add_end_date), slice(other.start_date, other.end_date)
        )
        add_self = [
            x + y for x, y in zip(added_timeseries.data[self_slice_interval], self.data)
        ]
        added_timeseries.data[self_slice_interval] = add_self

        add_other = [
            x + y
            for x, y in zip(added_timeseries.data[other_slice_interval], other.data)
        ]
        added_timeseries.data[other_slice_interval] = add_other

        return added_timeseries

    def __sub__(self, other):
        negated_other = Timeseries(
            start_date=other.start_date,
            end_date=other.end_date,
            data=[-x for x in other.data],
        )
        return self + negated_other

    def __mul__(self, other):
        mul_start_date = max(self.start_date, other.start_date)
        mul_end_date = min(self.end_date, other.end_date)
        mul_timeseries = Timeseries(
            start_date=mul_start_date,
            end_date=mul_end_date,
            data=[1] * months_in_interval(mul_start_date, mul_end_date),
        )
        self_slice_interval = get_slice_indexes_from_date_intervals(
            slice(self.start_date, self.end_date), slice(mul_start_date, mul_end_date)
        )
        other_slice_interval = get_slice_indexes_from_date_intervals(
            slice(other.start_date, other.end_date), slice(mul_start_date, mul_end_date)
        )
        mul_timeseries.data = [
            x * y for x, y in zip(mul_timeseries.data, self.data[self_slice_interval])
        ]

        mul_timeseries.data = [
            x * y for x, y in zip(mul_timeseries.data, other.data[other_slice_interval])
        ]

        return mul_timeseries

    def __truediv__(self, other):
        inverse_other = Timeseries(
            start_date=other.start_date,
            end_date=other.end_date,
            data=[1 / x for x in other.data],
        )
        return self * inverse_other

    def __getitem__(self, key: slice | date):
        """Implement slicing and indexing"""

        if isinstance(key, date):
            data_index = months_in_interval(self.start_date, key) - 1
            return self.data[data_index]

        time_range = key
        slice_interval = get_slice_indexes_from_date_intervals(
            slice(self.start_date, self.end_date),
            slice(time_range.start, time_range.stop),
        )
        # Slice the data list based on the calculated indices
        sliced_data = self.data[slice_interval]

        # Create and return the sliced Timeseries
        return Timeseries(
            start_date=time_range.start, end_date=time_range.stop, data=sliced_data
        )

    @property
    def pd_timeseries(self):
        range = pd.date_range(self.start_date, self.end_date, freq="ME")
        return pd.Series(self.data, index=range)


def constant_timeseries(value: float, start: date, end: date) -> Timeseries:
    data = [value] * months_in_interval(start, end)
    return Timeseries(
        start_date=start,
        end_date=end,
        data=data,
    )


def linear_timeseries(
    a: float, b: float, start: date, end: date
) -> Timeseries:
    """computes a linear timeseries

    f(t) = a + b*t

    Args:
        a (float): initial value
        b (float): slope of the function
        start (date):
        end (date):

    Returns:
        Timeseries: resulting timeseries
    """
    data = []
    for t in range(0, months_in_interval(start, end)):
        data[t] = a + b*t

    return Timeseries(
        start_date=start,
        end_date=end,
        data=data,
    )
