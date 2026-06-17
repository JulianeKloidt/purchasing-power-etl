import pandas as pd

from database.connection import DatabaseConnection


class IndicatorValuesLoader:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def load(self, df: pd.DataFrame) -> None:

        records = [
            (
                row["country_code"],
                row["indicator_code"],
                row["year"],
                row["value"],
            )
            for _, row in df.iterrows()
        ]

        with self.db.connect() as conn:
            with conn.cursor() as cur:

                cur.executemany(
                    """
                    INSERT INTO indicator_values (
                        country_code,
                        indicator_code,
                        year,
                        value
                    )
                    VALUES (%s, %s, %s, %s)

                    ON CONFLICT (
                        country_code,
                        indicator_code,
                        year
                    )
                    DO UPDATE
                    SET value = EXCLUDED.value
                    """,
                    records,
                )

            conn.commit()