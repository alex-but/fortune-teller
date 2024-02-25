"""Module for handling timeseries of data
"""

from ctypes import Union
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

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


def constant_timeseries(value: int, start: date, end: date) -> Timeseries:
    data = [value] * months_in_interval(start, end)
    return Timeseries(
        start_date=start,
        end_date=end,
        data=data,
    )
