import pandas as pd

from src.validation.validate import validate_data


def test_valid_data(tmp_path):

    data = {
        "id": [1],
        "title": ["Test Product"],
        "description": ["Test"],
        "category": ["test"],
        "price": [100],
        "discountPercentage": [10],
        "rating": [4.5],
        "stock": [20],
        "tags": ["test"],
        "brand": ["Test"],
        "sku": ["TEST-1"],
        "weight": [1],
        "dimensions": ["10x10x10"],
        "warrantyInformation": ["1 year"],
        "shippingInformation": ["Ships"],
        "availabilityStatus": ["In Stock"],
        "reviews": ["[]"],
        "returnPolicy": ["30 days"],
        "minimumOrderQuantity": [1],
        "meta": ["{}"]
    }

    file_path = (
        tmp_path /
        "test_products.csv"
    )

    pd.DataFrame(data).to_csv(
        file_path,
        index=False
    )

    assert bool(
        validate_data(str(file_path))
    )