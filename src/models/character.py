"""A characted definition"""

from dataclasses import dataclass
from .assets import Asset
from .timeseries import Timeseries


@dataclass
class Character:
    name: str
    assets: list[Asset]
    capital_g_Au: Timeseries
