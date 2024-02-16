import pytest
from datetime import date
from src.models.character import Character
from src.models.assets import RealEstateProperty, Loan
from src.models.timeseries import Timeseries, Period
from src.models.world import City, Country, Currency


@pytest.fixture
def sample_data():
    # Sample timeseries data
    ts = Timeseries(
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        period=Period.Daily,
        data=[100] * 365,
    )

    # Sample currency data
    currency = Currency(name="USD", interest_rate=ts, inflation=ts, units_per_g_Au=ts)

    # Sample country data
    country = Country(
        name="USA",
        currency=currency,
        real_estate_aquisition_cost_percentage=5,
        stock_index=ts,
    )

    # Sample city data
    city = City(
        name="New York",
        country=country,
        sqm_housing_price=ts,
        yearly_rent_to_price_index=ts,
    )

    # Sample assets
    asset1 = RealEstateProperty(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency="USD",
        sale_date=None,
        surface_sqm=44.2,
        city=city,
    )

    asset2 = Loan(
        initial_value=2000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
        end_date=date(2044, 1, 31),
    )
    assets = [asset1, asset2]

    return assets


def test_Character(sample_data):
    assets = sample_data
    character = Character(name="John Doe", assets=assets, initial_capital_g_Au=1000)
    assert character.name == "John Doe"
    assert character.assets == assets
    assert character.initial_capital_g_Au == 1000
