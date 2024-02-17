"""Module for handling timeseries of data
"""

from ctypes import Union
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

import pandas as pd


class Period(Enum):
    Daily: str = "D"
    Monthly: str = "ME"
    Yearly: str = "YE"


class DateOrderException(Exception):
    """End date is before the begnning date"""

    def __init__(self, start_date: date, end_date: date, message: str):
        self.start_date = start_date
        self.end_date = end_date
        self.message = message
        super().__init__(message)


class DataToPeriodMissmatch(Exception):
    """Show that data does not have the number of samples expected by a timeseries"""

    def __init__(
        self,
        start_date: date,
        end_date: date,
        period: Period,
        no_samples: int,
        message: str,
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.period = Period
        self.no_samples = no_samples
        self.message = message
        super().__init__(message)


@dataclass(kw_only=True)
class Timeseries:
    start_date: date = field(default_factory=date)
    end_date: date = field(default_factory=date)
    period: Period = field(default_factory=Period)
    data: list[float] = field(default_factory=list, repr=False)
    pd_timeseries: pd.Series = field(init=False, repr=False)

    def __post_init__(self):
        if self.start_date > self.end_date:
            raise DateOrderException(
                start_date=self.start_date,
                end_date=self.end_date,
                message=f"""start date {self.start_date} is later than
                            end date {self.end_date} in the timeseries""",
            )
        datetimeindex = pd.date_range(
            start=self.start_date, end=self.end_date, freq=self.period.value
        )

        if len(datetimeindex) != len(self.data):
            raise DataToPeriodMissmatch(
                start_date=self.start_date,
                end_date=self.end_date,
                period=self.period,
                no_samples=len(self.data),
                message=f"""Cannot initialize timeseries with the given data. The length
                        of the data {len(datetimeindex)} does not mactch the number of 
                        samples from the period: {len(self.data)}""",
            )
        self.pd_timeseries = pd.Series(self.data, index=datetimeindex)
