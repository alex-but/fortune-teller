import pytest
from datetime import date
from src.models.assets import (
    Job,
    Stream,
    Asset,
    Stock,
    RealEstateProperty,
    CommodityBundle,
    Saving,
    Loan,
)
from src.models.timeseries import (
    Timeseries,
    constant_increase_timeseries,
    constant_timeseries,
    months_in_interval,
)
from src.models.world import City, Commodity, Country, Currency


@pytest.fixture
def sample_data():
    # Sample timeseries data
    ts = Timeseries(
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        data=[100] * 12,
    )

    # Sample currency data
    currency = Currency(name="USD", interest_rate=ts, units_per_g_Au=ts)

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

    return currency, country, city, commodity, ts


def test_Stream(sample_data):
    currency, _, _, _, ts = sample_data
    stream = Stream(stream_value=ts, currency=currency)
    assert stream.stream_value == ts
    assert stream.currency == currency


def test_StockBundle(sample_data):
    currency, country, _, _, _ = sample_data
    stock_bundle = Stock(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
        country=country,
    )
    assert stock_bundle.initial_value == 1000
    assert stock_bundle.purchase_date == date(2022, 1, 1)
    assert stock_bundle.sale_date is None
    assert stock_bundle.currency == currency
    assert stock_bundle.country == country


def test_RealEstateProperty(sample_data):
    currency, _, city, _, _ = sample_data
    real_estate_property = RealEstateProperty(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
        city=city,
        surface_sqm=55.4,
    )
    assert real_estate_property.initial_value == 1000
    assert real_estate_property.purchase_date == date(2022, 1, 1)
    assert real_estate_property.sale_date is None
    assert real_estate_property.currency == currency
    assert real_estate_property.city == city
    assert real_estate_property.surface_sqm == 55.4


def test_CommodityBundle(sample_data):
    currency, _, _, commodity, _ = sample_data
    commodity_bundle = CommodityBundle(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
        commodity=commodity,
    )
    assert commodity_bundle.initial_value == 1000
    assert commodity_bundle.purchase_date == date(2022, 1, 1)
    assert commodity_bundle.sale_date is None
    assert commodity_bundle.currency == currency
    assert commodity_bundle.commodity == commodity


def test_Saving(sample_data):
    currency, _, _, _, _ = sample_data
    saving = Saving(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
    )
    assert saving.initial_value == 1000
    assert saving.purchase_date == date(2022, 1, 1)
    assert saving.sale_date is None
    assert saving.currency == currency


def test_Loan(sample_data):
    currency, _, _, _, _ = sample_data
    loan = Loan(
        initial_value=-1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=date(2022, 12, 31),
        end_date=date(2023, 12, 31),
    )
    assert loan.initial_value == -1000
    assert loan.purchase_date == date(2022, 1, 1)
    assert loan.sale_date == date(2022, 12, 31)
    assert loan.currency == currency
    assert loan.end_date == date(2023, 12, 31)


def test_job(sample_data):
    currency, _, _, _, _ = sample_data
    job = Job(
        initial_value=-1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=date(2022, 12, 31),
        monthly_saving=300,
    )

    expected_stream = constant_timeseries(300, date(2022, 1, 1), date(2022, 12, 31))
    stream = job.stream_g_Au
    assert stream.data == expected_stream.data
    assert job.initial_value == -1000
    assert job.purchase_date == date(2022, 1, 1)
    assert job.sale_date == date(2022, 12, 31)
    assert job.currency == currency
    assert job.monthly_saving == 300


def test_stock_value():
    """stock value is a timeseries in g Au that depend on the stock country currency.

    Testing one year of data with all values constant"""
    start = date(2024, 1, 1)
    end = date(2024, 12, 31)
    euro = Currency(
        name="EUR",
        interest_rate=constant_timeseries(0.03, start, end),
        units_per_g_Au=constant_timeseries(10, start, end),
    )
    Germany = Country(
        name="DE",
        currency=euro,
        real_estate_acquisition_cost_percentage=9,
        stock_index=constant_increase_timeseries(
            first_value=3, monthly_increase_rate=0.012, start=start, end=end
        ),
    )

    stock = Stock(
        initial_value=100,
        purchase_date=start,
        sale_date=end,
        country=Germany,
        currency=euro,
    )

    stock_value = stock.value_g_Au
    assert len(stock_value.data) == months_in_interval(start, end)
    assert stock_value[start] == (100) * (1 / 10)
    # second month stock have increased by 1.2%
    assert stock_value[date(start.year, start.month + 1, start.day)] == 100 * (
        1 + 0.012
    ) * (1 / 10)
