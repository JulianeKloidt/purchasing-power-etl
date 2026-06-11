import pandas as pd


INVALID_CODES = ["WLD", "HIC", "LIC", "MIC", "AFE", "AFW", "ARB"]


def transform_worldbank_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw World Bank API data into analytics-ready format.
    """

    # 1. Drop missing values (Option A)
    df = df.dropna(subset=["value"])

    # 2. Remove aggregates / economic groupings
    df = df[~df["country_code"].isin(INVALID_CODES)]

    # 3. Type enforcement
    df["year"] = df["year"].astype(int)
    df["value"] = df["value"].astype(float)

    return df