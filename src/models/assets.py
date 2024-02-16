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
    """A stock asset owned by a character"""

    initial_value: int
    cost: int  # cost is how much you pay for it, value is how much is worth
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
