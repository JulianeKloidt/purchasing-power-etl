import sys
import pytest
import os
from psycopg.errors import UniqueViolation
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parents[1] / "src")
)

from database.connection import DatabaseConnection
from repositories.indicator_repository import IndicatorRepository

USER = os.getenv("DB_USER")

TEST_DB = DatabaseConnection(
    dbname=os.getenv("DB_NAME", "purchasing_power_test"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.getenv("DB_PASSWORD", "postgres"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", 5432)),
)

def setup_base():
    with TEST_DB.connect() as conn:
        with conn.cursor() as cur:

            # Clean tables (order matters due to FK constraints)
            cur.execute("DELETE FROM indicator_values")
            cur.execute("DELETE FROM indicators")
            cur.execute("DELETE FROM countries")

            # Insert country
            cur.execute(
                """
                INSERT INTO countries (
                    country_code,
                    country_name,
                    entity_type,
                    region
                )
                VALUES (
                    'KEN',
                    'Kenya',
                    'country',
                    'Sub-Saharan Africa'
                )
                """
            )

            # Insert indicator
            cur.execute(
                """
                INSERT INTO indicators (
                    indicator_code,
                    indicator_name
                )
                VALUES (
                    'TEST.CPI',
                    'Test CPI'
                )
                """
            )

def insert_observation(value):
    with TEST_DB.connect() as conn:
        with conn.cursor() as cur:

            cur.execute(
                """
                INSERT INTO indicator_values (
                    country_code,
                    indicator_code,
                    year,
                    value
                )
                VALUES (%s, %s, %s, %s)
                """,
                (
                    "KEN",
                    "TEST.CPI",
                    2020,
                    value,
                ),
            )

def test_get_value_success():

    setup_base()
    insert_observation(100.0)

    repo = IndicatorRepository(TEST_DB)

    value = repo.get_value(
        "KEN",
        "TEST.CPI",
        2020,
    )

    assert value == 100.0

def test_get_value_missing_observation():

    setup_base()

    repo = IndicatorRepository(TEST_DB)

    with pytest.raises(ValueError) as exc_info:
        repo.get_value(
        "KEN",
        "TEST.CPI",
        1999
    )
    
    assert "No observation found" in str(exc_info.value)

def test_get_value_null_value():

    setup_base()
    insert_observation(None)

    repo = IndicatorRepository(TEST_DB)

    with pytest.raises(ValueError) as exc_info:
        repo.get_value(
        "KEN",
        "TEST.CPI",
        2020
    )
    
    assert "Observation exists but value is missing" in str(exc_info.value)


def test_duplicate_insert_fails():

    setup_base()

    insert_observation(100.0)

    with pytest.raises(UniqueViolation):
        insert_observation(100.0)