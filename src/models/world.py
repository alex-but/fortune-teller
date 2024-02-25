"""Definitions of world elements relevant for financial simulations
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Callable, Union
import pandas as pd
from enum import Enum
from .timeseries import Timeseries


@dataclass(frozen=True, kw_only=True)
class Currency:
    name: str
    interest_rate: Timeseries
    inflation: Timeseries
    units_per_g_Au: Timeseries


@dataclass(frozen=True, kw_only=True)
class Country:
    name: str
    currency: Currency
    real_estate_acquisition_cost_percentage: int
    stock_index: Timeseries


@dataclass(frozen=True, kw_only=True)
class City:
    name: str
    country: Country
    sqm_housing_price: Timeseries
    yearly_rent_to_price_index: Timeseries


@dataclass(frozen=True, kw_only=True)
class Commodity:
    """A commodity like gold, silver etc."""

    name: str
    units_per_g_Au: Timeseries


@dataclass(frozen=True, kw_only=True)
class World:
    name: str
    currencies: list[Currency]
    countries: list[Country]
    cities: list[City]
    comodities: list[Commodity]
