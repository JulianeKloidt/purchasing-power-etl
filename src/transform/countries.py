import pandas as pd

def transform_countries(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform country metadata from the World Bank API
    into a format ready for PostgreSQL loading.
    """

    # Step 1: validate required columns
    required_columns = {
        "country_code",
        "country_name",
        "region"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    # Step 2: validate region values
    if df["region"].isna().any():
        raise ValueError(
            "Found null values in region column."
        )

    # Step 3: create entity_type
    df["entity_type"] = (
        df["region"]
        .eq("Aggregates")
        .map({
            True: "aggregate",
            False: "country"
        })
    )

    # Step 4: check duplicates
    duplicate_count = df.duplicated(
        subset=["country_code"]
    ).sum()

    if duplicate_count > 0:
        print(
            f"Warning: found {duplicate_count} duplicate country codes."
        )
        df = df.drop_duplicates(
            subset=["country_code"]
        )

    # Step 5: return final columns
    return df[
        [
            "country_code",
            "country_name",
            "region",
            "entity_type"
        ]
    ]