"""Data model for assets that can be held by a character
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from .timeseries import Frequency, Timeseries, get_samples_in_period
from .world import City, Comodity, Country, Currency


@dataclass
class Stream:
    """A stream of cash. Can be positive (revenue) or negative (expense)"""

    stream_value: Timeseries
    currency: Currency


@dataclass(frozen=True, kw_only=True)
class Asset(ABC):
    """A stock asset owned by a character. The ownership is related to a
    specific duration of time"""

    initial_value: int
    purchase_date: date
    currency: Currency
    sale_date: date

    @property
    @abstractmethod
    def stream(self) -> Timeseries:
        """returns the revenue (positive) or expense (negative) stream produced by the asset"""


def constant_asset_stream(value: int, asset: Asset) -> Timeseries:
    frequency = Frequency.Monthly
    data = [value] * get_samples_in_period(
        asset.purchase_date, asset.sale_date, frequency
    )
    return Timeseries(
        start_date=asset.purchase_date,
        end_date=asset.sale_date,
        frequency=frequency,
        data=data,
    )


@dataclass(frozen=True, kw_only=True)
class Stock(Asset):
    """A stock asset owned by a character"""

    country: Country

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)


@dataclass(frozen=True, kw_only=True)
class RealEstateProperty(Asset):
    """A property owned by a character"""

    city: City
    surface_sqm: float

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)


@dataclass(frozen=True, kw_only=True)
class ComodityBundle(Asset):
    """A comodity asset owned by a character"""

    commodity: Comodity

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)


@dataclass(frozen=True, kw_only=True)
class Saving(Asset):
    """Saving account. All sales should result in a new saving"""

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)


@dataclass(frozen=True, kw_only=True)
class Loan(Asset):
    """Represents a loan. Will have a negative value and a negative cost"""

    end_date: date

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)


@dataclass(frozen=True, kw_only=True)
class Job(Asset):
    """A job is an asset producing money but is not vandable.
    For the purpose of this program we only consider what are
    the savings produced by a job"""

    monthly_saving: int

    @property
    def stream(self) -> Timeseries:
        return constant_asset_stream(0)
