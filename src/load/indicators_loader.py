import pandas as pd

from database.connection import DatabaseConnection


class IndicatorsLoader:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def load(self, df: pd.DataFrame) -> None:

        with self.db.connect() as conn:
            with conn.cursor() as cur:

                for _, row in df.iterrows():

                    cur.execute(
                        """
                        INSERT INTO indicators (
                            indicator_code,
                            indicator_name
                        )
                        VALUES (%s, %s)
                        ON CONFLICT (indicator_code)
                        DO NOTHING
                        """,
                        (
                            row["indicator_code"],
                            row["indicator_name"],
                        ),
                    )

            conn.commit()