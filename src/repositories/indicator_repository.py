from database.connection import DatabaseConnection


class IndicatorRepository:

    def __init__(
        self,
        db: DatabaseConnection
    ):
        self.db = db

    def get_value(
        self,
        country_code: str,
        indicator_code: str,
        year: int
    ) -> float:

        with self.db.connect() as conn:
            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT value
                    FROM indicator_values
                    WHERE country_code = %s
                    AND indicator_code = %s
                    AND year = %s
                    """,
                    (country_code, indicator_code, year)
                )

                results = cur.fetchone()

        if results is None:
            raise ValueError(
                f"No observation found for {country_code}, "
                f"{indicator_code}, {year}."
            )

        value = results[0]

        if value is None:
            raise ValueError(
                f"Observation exists but value is missing for "
                f"{country_code}, {indicator_code}, {year}."
            )

        return float(value)