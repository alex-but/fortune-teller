"""A characted definition"""

from dataclasses import dataclass
from assets import Asset


@dataclass
class Character:
    name: str
    assets: list[Asset]
