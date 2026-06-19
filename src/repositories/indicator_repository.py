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
                    (
                        country_code,
                        indicator_code,
                        year,
                    )
                )

                results = cur.fetchall()

        if len(results) == 0:
            raise ValueError(
                f"No observation found for "
                f"{country_code}, "
                f"{indicator_code}, "
                f"{year}."
            )

        if len(results) > 1:
            raise ValueError(
                f"More than one observation found for "
                f"{country_code}, "
                f"{indicator_code}, "
                f"{year}."
            )

        value = results[0][0]

        if value is None:
            raise ValueError(
                f"Observation exists but value is missing for "
                f"{country_code}, "
                f"{indicator_code}, "
                f"{year}."
            )

        return float(value)




    
        
        
    
        