"""Data model for assets that can be held by a character
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date

from .timeseries import Timeseries
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
    sale_date: date | None


@dataclass(frozen=True, kw_only=True)
class StockBundle(Asset):
    """A stock asset owned by a character"""

    country: Country


@dataclass(frozen=True, kw_only=True)
class RealEstateProperty(Asset):
    """A property owned by a character"""

    city: City
    surface_sqm: float


@dataclass(frozen=True, kw_only=True)
class ComodityBundle(Asset):
    """A comodity asset owned by a character"""

    commodity: Comodity


@dataclass(frozen=True, kw_only=True)
class Saving(Asset):
    """Saving account. All sales should result in a new saving"""


@dataclass(frozen=True, kw_only=True)
class Loan(Asset):
    """Represents a loan. Will have a negative value and a negative cost"""

    end_date: date


@dataclass(frozen=True, kw_only=True)
class Job(Asset):
    """A job is an asset producing money but is not vandable.
    For the purpose of this program we only consider what are
    the savings produced by a job"""

    monthly_saving: int
