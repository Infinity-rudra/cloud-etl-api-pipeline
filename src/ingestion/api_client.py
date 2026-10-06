import time

import pandas as pd
import requests

from config.config import (
    API_LIMIT,
    API_MAX_RETRIES,
    API_TIMEOUT,
    API_URL
)


def extract_data():

    all_products = []
    skip = 0

    session = requests.Session()

    while True:

        params = {
            "limit": API_LIMIT,
            "skip": skip
        }

        for attempt in range(1, API_MAX_RETRIES + 1):

            try:

                response = session.get(
                    API_URL,
                    params=params,
                    timeout=API_TIMEOUT
                )

                response.raise_for_status()

                data = response.json()

                products = data.get(
                    "products",
                    []
                )

                break

            except requests.exceptions.RequestException as error:

                if attempt == API_MAX_RETRIES:
                    raise RuntimeError(
                        f"API request failed after "
                        f"{API_MAX_RETRIES} attempts: {error}"
                    )

                print(
                    f"API request failed. "
                    f"Retrying ({attempt}/{API_MAX_RETRIES})..."
                )

                time.sleep(2)

        if not products:
            break

        all_products.extend(products)

        print(
            f"Fetched {len(products)} records "
            f"(skip={skip})"
        )

        total = data.get("total", 0)

        skip += API_LIMIT

        if skip >= total:
            break

    session.close()

    df = pd.DataFrame(all_products)

    if df.empty:
        raise RuntimeError(
            "API returned no product records."
        )

    print("\nAPI data extracted successfully.")
    print("Total Rows:", len(df))
    print("Total Columns:", len(df.columns))

    output_file = "data/raw/products_raw.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(
        "Raw data saved:",
        output_file
    )

    return df