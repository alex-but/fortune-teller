"""A characted definition"""

from dataclasses import dataclass

from .world import Currency
from .assets import Asset
from .timeseries import Timeseries


@dataclass
class Character:
    name: str
    assets: list[Asset]
    initial_capital_g_Au: float

    @property
    def capital_g_Au(self) -> Timeseries:
        """TODO computed capital over time"""
        pass

    @property
    def wealth(self, currency: Currency) -> Timeseries:
        """TODO wealth over time of the character in a give
        currency.
        """
        pass
