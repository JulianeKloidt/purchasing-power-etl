import pandas as pd

from database.connection import DatabaseConnection


class CountriesLoader:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def load(self, df: pd.DataFrame) -> None:

        with self.db.connect() as conn:
            with conn.cursor() as cur:

                for _, row in df.iterrows():

                    cur.execute(
                        """
                        INSERT INTO countries (
                            country_code,
                            country_name,
                            entity_type,
                            region
                        )
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (country_code)
                        DO NOTHING
                        """,
                        (
                            row["country_code"],
                            row["country_name"],
                            row["entity_type"],
                            row["region"],
                        ),
                    )

            conn.commit()