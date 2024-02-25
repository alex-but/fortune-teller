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
    """ Country object to define country specific indicators.
    
    Arguments:
        name (str): name of the country
        currency (Currency): the currency used in this country
        real_estate_acquisition_cost_percentage (int): percentage of real estate value
            payed as taxes when buying real estate
        stock_index: appreciation of the main stock index over time relative to an arbitrary
            moment
    """
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
