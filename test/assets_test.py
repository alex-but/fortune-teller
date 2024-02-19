import pytest
from datetime import date
from src.models.assets import (
    Job,
    Stream,
    Asset,
    Stock,
    RealEstateProperty,
    ComodityBundle,
    Saving,
    Loan,
)
from src.models.timeseries import Timeseries, Frequency, constant_timeseries
from src.models.world import City, Comodity, Country, Currency


@pytest.fixture
def sample_data():
    # Sample timeseries data
    ts = Timeseries(
        start_date=date(2022, 1, 1),
        end_date=date(2022, 12, 31),
        frequency=Frequency.Daily,
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

    # Sample comodity data
    comodity = Comodity(name="Gold", units_per_g_Au=ts)

    return currency, country, city, comodity, ts


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


def test_ComodityBundle(sample_data):
    currency, _, _, comodity, _ = sample_data
    comodity_bundle = ComodityBundle(
        initial_value=1000,
        purchase_date=date(2022, 1, 1),
        currency=currency,
        sale_date=None,
        commodity=comodity,
    )
    assert comodity_bundle.initial_value == 1000
    assert comodity_bundle.purchase_date == date(2022, 1, 1)
    assert comodity_bundle.sale_date is None
    assert comodity_bundle.currency == currency
    assert comodity_bundle.commodity == comodity


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

    expected_stream = constant_timeseries(
        300, date(2022, 1, 1), date(2022, 12, 31), Frequency.Monthly
    )
    stream = job.stream_g_Au
    assert stream.data == expected_stream.data
    assert job.initial_value == -1000
    assert job.purchase_date == date(2022, 1, 1)
    assert job.sale_date == date(2022, 12, 31)
    assert job.currency == currency
    assert job.monthly_saving == 300
