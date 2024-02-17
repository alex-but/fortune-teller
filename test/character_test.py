import datetime
import sre_compile
import pytest
from datetime import date, timedelta
from src.models.character import Character
from src.models.assets import RealEstateProperty, Loan
from src.models.timeseries import DateOrderException, Timeseries, Period
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
    start_investment_date = date(2024, 1, 31)
    end_of_life = date(2025, 1, 31)
    return assets, start_investment_date, end_of_life


def test_Character(sample_data):
    assets, start_investment_date, end_of_life = sample_data
    character = Character(
        name="John Doe",
        assets=assets,
        start_investment_date=start_investment_date,
        end_of_life=end_of_life,
        initial_capital_g_Au=1000,
    )
    assert character.name == "John Doe"
    assert character.assets == assets
    assert character.initial_capital_g_Au == 1000
    assert character.end_of_life == end_of_life
    assert character.start_investment_date == start_investment_date


def test_invalid_Character(sample_data):
    assets, start_investment_date, _ = sample_data
    too_early_end_of_life = start_investment_date - timedelta(days=1)
    with pytest.raises(DateOrderException):
        Character(
            name="John Doe",
            start_investment_date=start_investment_date,
            end_of_life=too_early_end_of_life,
        )
