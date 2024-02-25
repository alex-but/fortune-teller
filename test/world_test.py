import pytest
from datetime import date
from src.models.world import Currency, Country, City, Commodity, World
from src.models.timeseries import Timeseries


@pytest.fixture
def sample_data():
    # Sample timeseries data
    ts = Timeseries(
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        data=[100] * 12,
    )

    # Sample currency data
    currency = Currency(name="USD", interest_rate=ts, inflation=ts, units_per_g_Au=ts)

    # Sample country data
    country = Country(
        name="USA",
        currency=currency,
        real_estate_acquisition_cost_percentage=5,
        stock_index=ts,
    )

    # Sample city data
    city = City(
        name="New York",
        country=country,
        sqm_housing_price=ts,
        yearly_rent_to_price_index=ts,
    )

    # Sample commodity data
    commodity = Commodity(name="Gold", units_per_g_Au=ts)

    # Sample world data
    world = World(
        name="Earth",
        currencies=[currency],
        countries=[country],
        cities=[city],
        comodities=[commodity],
    )

    return currency, country, city, commodity, world


def test_Currency(sample_data):
    currency, _, _, _, _ = sample_data
    assert currency.name == "USD"
    assert currency.interest_rate.start_date == date(2022, 1, 1)


def test_Country(sample_data):
    _, country, _, _, _ = sample_data
    assert country.name == "USA"
    assert country.currency.name == "USD"


def test_City(sample_data):
    _, _, city, _, _ = sample_data
    assert city.name == "New York"
    assert city.country.name == "USA"


def test_Commodity(sample_data):
    _, _, _, commodity, _ = sample_data
    assert commodity.name == "Gold"


def test_World(sample_data):
    _, _, _, _, world = sample_data
    assert world.name == "Earth"
    assert len(world.currencies) == 1
    assert len(world.countries) == 1
    assert len(world.cities) == 1
    assert len(world.comodities) == 1
