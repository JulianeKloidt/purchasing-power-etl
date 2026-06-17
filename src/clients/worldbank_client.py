import requests
import pandas as pd
import time


class WorldBankClient:
    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self, per_page: int = 1000):
        self.per_page = per_page

    # get indicator data
    def get_indicator_data(self, indicator: str):
        all_records = []

        # Step 1: request page 1
        response = requests.get(
            f"{self.BASE_URL}/country/all/indicator/{indicator}",
            params={
                "format": "json",
                "per_page": self.per_page,
                "page": 1
            }
        )

        data = response.json()
        meta = data[0]
        total_pages = meta["pages"]

        # Step 2: loop through all pages
        for page in range(1, total_pages + 1):
            for attempt in range(3):
                response = requests.get(
                    f"{self.BASE_URL}/country/all/indicator/{indicator}",
                    params={
                        "format": "json",
                        "per_page": self.per_page,
                        "page": page
                    }
                )

                if response.status_code == 200:
                    try:
                        data = response.json()
                        break
                    except:
                        pass

                time.sleep(1)

            data = response.json()
            records = data[1]
            all_records.extend(records)

        # Step 3: build dataframe
        df = pd.DataFrame(all_records)

        # Step 4: flatten structure
        df["country_code"] = df["countryiso3code"]
        df["indicator_code"] = df["indicator"].apply(lambda x: x["id"])
        df = df[["country_code", "indicator_code", "date", "value"]]
        df = df.rename(columns={"date": "year"})
        df["year"] = df["year"].astype(int)

        return df

    # get multiple indicators
    def get_multiple_indicators(
            self,
            indicators: list[str]
            ) -> pd.DataFrame:
        dfs = []

        for indicator in indicators:
            df = self.get_indicator_data(indicator)
            dfs.append(df)

        return pd.concat(
            dfs,
            ignore_index=True
        )

    # get country meta-data
    def get_countries(self):
            all_records = []

            # Step 1: request page 1
            response = requests.get(
                f"{self.BASE_URL}/country/all",
                params={
                    "format": "json",
                    "per_page": self.per_page,
                    "page": 1
                }
            )

            data = response.json()
            meta = data[0]
            total_pages = meta["pages"]

            # Step 2: loop through all pages
            for page in range(1, total_pages + 1):
                for attempt in range(3):
                    response = requests.get(
                        f"{self.BASE_URL}/country/all",
                        params={
                            "format": "json",
                            "per_page": self.per_page,
                            "page": page
                        }
                    )

                    if response.status_code == 200:
                        try:
                            data = response.json()
                            break
                        except:
                            pass

                    time.sleep(1)

                data = response.json()
                records = data[1]
                all_records.extend(records)

            # Step 3: build dataframe
            df = pd.DataFrame(all_records)

            # Step 4: flatten structure
            df["country_code"] = df["id"]
            df["country_name"] = df["name"]
            df["region"] = df["region"].apply(lambda x: x["value"])

            df = df[["country_code", "country_name", "region"]]

            return df

    # get indicator meta-data   
    def get_indicator_metadata(
        self,
        indicators: list[str]
    ) -> list[dict]:

        all_records = []

        for indicator in indicators:

            response = requests.get(
                f"{self.BASE_URL}/indicator/{indicator}",
                params={"format": "json"}
            )

            response = requests.get(
                f"{self.BASE_URL}/indicator/{indicator}",
                params={"format": "json"}
                )

            if response.status_code != 200:
                raise RuntimeError(
                    f"Request failed for indicator {indicator}. "
                    f"Status code: {response.status_code}"
                )

            try:
                data = response.json()
            except Exception as e:
                raise RuntimeError(
                    f"Failed to parse JSON for indicator {indicator}"
                ) from e

            try:
                record = data[1][0]
            except:
                raise TypeError("Data in wrong format")

            if record["id"] != indicator:
                raise ValueError("Mismatched indicator id.")

            all_records.append(
                {
                    "indicator_code": record["id"],
                    "indicator_name": record["name"]
                }
            )

        return all_records
    