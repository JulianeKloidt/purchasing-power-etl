import pandas as pd


def transform_indicator_values(
    df: pd.DataFrame
) -> pd.DataFrame:
    """
    Clean indicator observations for loading
    into PostgreSQL.
    """

    required_columns = {
        "country_code",
        "indicator_code",
        "year",
        "value",
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if df["country_code"].isna().any():
        raise ValueError(
            "Found null country codes."
        )

    if df["indicator_code"].isna().any():
        raise ValueError(
            "Found null indicator codes."
        )

    if df["year"].isna().any():
        raise ValueError(
            "Found null years."
        )

    df = df[df["country_code"] != ""]

    duplicate_count = df.duplicated(
        subset=[
            "country_code",
            "indicator_code",
            "year",
        ]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate observations."
        )

    return df