import pandas as pd


def transform_indicators(
    records: list[dict]
) -> pd.DataFrame:
    """
    Transform indicator metadata into a format
    ready for PostgreSQL loading.
    """

    df = pd.DataFrame(records)

    required_columns = {
        "indicator_code",
        "indicator_name"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: "
            f"{sorted(missing_columns)}"
        )

    if df["indicator_code"].isna().any():
        raise ValueError(
            "Found null values in indicator_code."
        )

    if df["indicator_name"].isna().any():
        raise ValueError(
            "Found null values in indicator_name."
        )

    duplicate_count = df.duplicated(
        subset=["indicator_code"]
    ).sum()

    if duplicate_count > 0:
        raise ValueError(
            f"Found {duplicate_count} duplicate "
            f"indicator codes."
        )

    return df[
        [
            "indicator_code",
            "indicator_name"
        ]
    ]