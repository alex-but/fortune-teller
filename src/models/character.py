"""A characted definition"""

from dataclasses import dataclass, field
from datetime import date

from .world import Currency
from .assets import Asset
from .timeseries import DateOrderException, Timeseries


@dataclass
class Character:
    name: str
    start_investment_date: date
    end_of_life: date
    initial_capital_g_Au: float = 0
    assets: list[Asset] = field(default_factory=list)

    def __post_init__(self):
        if self.start_investment_date > self.end_of_life:
            raise DateOrderException(
                start_date=self.start_investment_date,
                end_date=self.end_of_life,
                message=f"""Character's start investment date {self.start_investment_date}
                         is later than its end of life {self.end_of_life}""",
            )

    @property
    def capital_g_Au(self) -> Timeseries:
        """TODO computed capital over time. This is the initial capital summed up with all the
        streams produced by the owned assets. This capital can never be negative. An ownership
        cannot be added or removed if it produces a negative capital value"""
        pass

    @property
    def wealth(self, currency: Currency) -> Timeseries:
        """TODO computed wealth over time of the character in a give
        currency.
        """
        pass

    def add_ownership(self, asset: Asset) -> None:
        """adds an asset ownership to the character. The asset should
        contain the purchase and sale time.

        raises:
        * sale exceed end of life
        * asset cannot be added at date: lack of funds
        """
        pass

    def remove_ownership(self, asset: Asset) -> None:
        """removes an asset ownership to the character. The asset should
        contain the purchase and sale time.

        raises:
        * asset removal produces a negative capital balance (e.g. lack of funds if
                a loan is removed)
        """
        pass
