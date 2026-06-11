import requests
import pandas as pd
import time


class WorldBankClient:
    BASE_URL = "https://api.worldbank.org/v2"

    def __init__(self, per_page: int = 1000):
        self.per_page = per_page

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