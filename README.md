![CI](https://github.com/julianekloidt/purchasing-power-etl/actions/workflows/ci.yml/badge.svg)

# Purchasing Power ETL

A Python-based ETL and analytics pipeline that retrieves Purchasing Power Parity (PPP) and Consumer Price Index (CPI) data from the World Bank API, stores the data in PostgreSQL, and provides reusable analytical methods for comparing monetary values across countries and time.

---

## Project Overview

Economists frequently need to compare monetary values collected in different countries and years. This project automates the process by:

* Extracting PPP and CPI data from the World Bank API
* Transforming and validating the raw data
* Loading the data into a normalized PostgreSQL database
* Providing an analytics layer for inflation adjustment and purchasing power conversion
* Supporting automated testing using pytest

The project follows a modular ETL architecture with clear separation between extraction, transformation, loading, database access, and business logic.

---

## Features

### Data Extraction

* Extracts country metadata from the World Bank API
* Extracts CPI (Consumer Price Index) data
* Extracts PPP conversion factor data
* Retrieves indicator metadata directly from the API

### Data Transformation

* Validates required columns
* Detects duplicate observations
* Distinguishes countries from aggregate regions
* Cleans and standardizes API responses
* Preserves missing indicator values where they have analytical meaning

### Data Loading

* Loads data into PostgreSQL
* Uses primary and foreign key constraints
* Prevents duplicate observations
* Supports repeatable ETL execution

### Analytics Layer

The project currently supports three analytical methods:

* Inflation adjustment
* Conversion to International Dollars
* Conversion from historical local currency into target-year International Dollars

Example:

```python
service.to_target_year_international_dollars(
    amount=50,
    country_code="KEN",
    source_year=2015,
    target_year=2024
)
```

---

## Database Schema

The project uses a normalized relational schema consisting of three tables:

### countries

Stores metadata for countries and aggregate regions.

| Column        | Description                                    |
| ------------- | ---------------------------------------------- |
| country_code  | ISO3 country code or World Bank aggregate code |
| country_name  | Country or region name                         |
| entity_type   | Country or aggregate                           |
| region        | World Bank region                              |
| currency_code | Optional currency code                         |

### indicators

Stores indicator metadata.

| Column         | Description               |
| -------------- | ------------------------- |
| indicator_code | World Bank indicator code |
| indicator_name | Indicator description     |

### indicator_values

Stores yearly observations.

| Column         | Description          |
| -------------- | -------------------- |
| country_code   | Country identifier   |
| indicator_code | Indicator identifier |
| year           | Observation year     |
| value          | Indicator value      |

A composite uniqueness constraint prevents duplicate observations for the same country, indicator and year.

---

## Project Structure

```
src/
│
├── clients/
│   └── worldbank_client.py
│
├── database/
│   ├── connection.py
│   └── schema.sql
│
├── loaders/
│
├── repositories/
│   └── indicator_repository.py
│
├── services/
│   └── purchasing_power_service.py
│
├── transformations/
│
└── settings.py

tests/
```

---

## Technologies

* Python
* PostgreSQL
* pandas
* psycopg
* requests
* pycountry
* pytest

---

## Design Principles

This project emphasizes:

* Modular architecture
* Separation of concerns
* Explicit validation
* Reusable business logic
* Database normalization
* Automated testing
* Scalability for additional World Bank indicators


---

## CI / Automated Testing

This project uses GitHub Actions to automatically run the test suite on every push and pull request to the main branch.

The CI pipeline:

* Spins up a PostgreSQL service container
* Installs project dependencies
* Runs the full pytest test suite
* Validates database integrity and ETL transformations
* CI Configuration

The workflow is defined in:

```
.github/workflows/ci.yml
```

Continuous Integration ensures that:

* All ETL transformations remain stable
* Database interactions behave as expected
* Changes do not break existing functionality
* The project remains reproducible across environments
* Running tests locally

You can also run the full test suite locally:

```
pytest -v
```
---

## Future Improvements

Potential extensions include:

* Additional World Bank indicators
* Currency metadata integration
* Docker support
* GitHub Actions for continuous integration
* Command-line interface
* REST API
* Data versioning
* Performance benchmarking

---

## Author

Developed by Juliane Kloidt.
