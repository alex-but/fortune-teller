"""Data model for assets that can be held by a character
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from .timeseries import (
    Timeseries,
    constant_timeseries,
)
from .world import City, Commodity, Country, Currency


@dataclass
class Stream:
    """A stream_g_Au of cash. Can be positive (revenue) or negative (expense)"""

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
    def stream_g_Au(self) -> Timeseries:
        """returns the revenue (positive) or expense (negative) stream_g_Au produced by the asset"""

    @property
    @abstractmethod
    def value_g_Au(self) -> Timeseries:
        """value of the asset over time measured in gold."""


@dataclass(frozen=True, kw_only=True)
class Stock(Asset):
    """A stock asset owned by a character"""

    country: Country

    @property
    def stream_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)

    @property
    def value_g_Au(self) -> Timeseries:
        initial_stock_value = self.country.stock_index[self.purchase_date]
        bought_units_ts = constant_timeseries(
            self.initial_value / initial_stock_value, self.purchase_date, self.sale_date
        )
        value_local_currency = bought_units_ts * self.country.stock_index
        value_g_Au = value_local_currency / self.country.currency.units_per_g_Au
        return value_g_Au


@dataclass(frozen=True, kw_only=True)
class RealEstateProperty(Asset):
    """A property owned by a character"""

    city: City
    surface_sqm: float

    @property
    def stream_g_Au(self) -> Timeseries:
        """TODO: computed value of the stream based on the country indicators"""
        return constant_timeseries(0, self.purchase_date, self.sale_date)

    @property
    def value_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)


@dataclass(frozen=True, kw_only=True)
class CommodityBundle(Asset):
    """A commodity asset owned by a character"""

    commodity: Commodity

    @property
    def stream_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)

    @property
    def value_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)


@dataclass(frozen=True, kw_only=True)
class Saving(Asset):
    """Saving account. All sales should result in a new saving"""

    @property
    def stream_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)

    @property
    def value_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)


@dataclass(frozen=True, kw_only=True)
class Loan(Asset):
    """Represents a loan. Will have a negative value_g_Au and a negative cost"""

    end_date: date

    @property
    def stream_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)

    @property
    def value_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)


@dataclass(frozen=True, kw_only=True)
class Job(Asset):
    """A job is an asset producing money but is not vendable.
    For the purpose of this program we only consider what are
    the savings produced by a job"""

    monthly_saving: int

    @property
    def stream_g_Au(self) -> Timeseries:
        return constant_timeseries(
            self.monthly_saving, self.purchase_date, self.sale_date
        )

    @property
    def value_g_Au(self) -> Timeseries:
        return constant_timeseries(0, self.purchase_date, self.sale_date)
