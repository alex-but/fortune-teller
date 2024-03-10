# Financial Simulation Data Models

This repository contains data models for a financial simulation, including definitions of assets, world elements, and timeseries.

## Asset Data Model

### Stream

- Represents a stream of cash, which can be positive (revenue) or negative (expense).
- Attributes:
  - `stream_value`: Timeseries object representing the value of the stream over time.
  - `currency`: Currency object representing the currency of the stream.

### Asset (Abstract)

- Abstract base class representing a generic asset owned by a character.
- Attributes:
  - `initial_value`: Initial total value of the asset.
  - `purchase_date`: Date when the asset was purchased.
  - `currency`: Currency object representing the currency of the asset.
  - `sale_date`: Optional date when the asset was sold.

### Stock

- Represents a stock asset owned by a character, bundled with information about the country.
- Inherits from Asset.
- Attributes:
  - `country`: Country object representing the country associated with the stock bundle.

### RealEstateProperty

- Represents a real estate property owned by a character, bundled with information about the city.
- Inherits from Asset.
- Attributes:
  - `city`: City object representing the city associated with the real estate property.
  - `surface_sqm`: size of the real estate.

### CommodityBundle

- Represents a commodity asset owned by a character, bundled with information about the commodity.
- Inherits from Asset.
- Attributes:
  - `commodity`: Commodity object representing the commodity associated with the bundle.

### Saving

- Represents a saving account owned by a character.
- Inherits from Asset.

### Loan

- Represents a loan owned by a character.
- Inherits from Asset.
- Attributes:
  - `end_date`: Date when the loan ends.

### Job

- Represents a job of a character.
- Attributes:
  - `monthly_saving`: how much of the job income can be saved.

## World Elements

### Currency

- Represents a currency used in the financial simulation.
- Attributes:
  - `name`: Name of the currency.
  - `interest_rate`: Timeseries representing the interest rate of the currency.
  - `units_per_g_Au`: Timeseries representing the units of the currency per gram of gold.

### Country

- Represents a country in the financial simulation.
- Attributes:
  - `name`: Name of the country.
  - `currency`: Currency object representing the currency used in the country.
  - `real_estate_acquisition_cost_percentage`: Percentage representing the cost of acquiring real estate properties in the country.
  - `stock_index`: Timeseries representing the stock index of the country.

### City

- Represents a city in the financial simulation.
- Attributes:
  - `name`: Name of the city.
  - `country`: Country object representing the country in which the city is located.
  - `sqm_housing_price`: Timeseries representing the price per square meter of housing in the city.
  - `yearly_rent_to_price_index`: Timeseries representing the yearly rent to price index ratio in the city.

### Commodity

- Represents a commodity like gold, silver, etc.
- Attributes:
  - `name`: Name of the commodity.
  - `units_per_g_Au`: Timeseries representing the units of the commodity per gram of gold.

### World

- Represents the world in the financial simulation, consisting of currencies, countries, cities, and commodities.
- Attributes:
  - `name`: Name of the world.
  - `currencies`: List of Currency objects in the world.
  - `countries`: List of Country objects in the world.
  - `cities`: List of City objects in the world.
  - `commodities`: List of Commodity objects in the world.

## Timeseries

- Represents a series of montlhy data points. Month and year of start date and end date are taken into consideration
- Attributes:
  - `start_date`: Start date of the timeseries.
  - `end_date`: End date of the timeseries.
  - `data`: List of data points.

## Character

- Represents a character in the financial simulation, which owns assets and has capital.
- Attributes:
  - `name`: Name of the character.
  - `assets`: List of Asset objects owned by the character.
  - `initial_capital_g_Au`: initial capital to start with.
  - `capital_g_Au`: Timeseries representing the capital (wealth) of the character over time in grams of gold.
  - `wealth`: computed total wealth over time in a given currency.

## Formulas

### Stocks
- The cash flow from stocks over time is constant and equal to zero. We consider that are no dividends; the stock value increases in value over time. The stream of cash over time in grams of gold (sg_Au) is:

$$s_{g/Au} = 0$$

- The value of the shares of a company's stock owned by a character changes over time depending on the stock price (st-pr). For instance, the value paid by one unit of stock on the purchase date (t=0) is:

$$S_{t=0} = st-pr_{t=0}$$

To calculate the value of the shares in grams of gold (Sg/Au) over time, we need to calculate the total units bought on the purchase date (units), and the value of these shares in the local currency (S).

The total of units bought on a specifc date is constant on time. If the character buy more shares from the same company's stocks, a new asset must be created.

$$units_{t=0} = total-amont-paid_{t=0}/st-pr_{t=0}$$

$$S_{t=t} = units_{t=0}*st-pr_{t=t}$$

$$S_{g/Au;t=t} = S_{t=t}/Au-pr_{g;t=t}$$


## Usage

To use the data models, simply import the required classes from the provided modules and create instances of the classes with the desired attributes. You can then use these instances to simulate financial scenarios, analyze the results, and visualize the data over time.

