import pandas as pd

from src.incremental.change_detector import (
    add_record_hash,
    detect_changes,
)


def test_record_hash_is_generated():
    df = pd.DataFrame([
        {
            "id": 1,
            "title": "Test Product",
            "description": "Test",
            "category": "test",
            "price": 100,
            "discountPercentage": 10,
            "rating": 4.5,
            "stock": 20,
            "brand": "Test",
            "sku": "TEST-001",
            "weight": 1,
            "width": 10,
            "height": 10,
            "depth": 10,
            "warrantyInformation": "1 year",
            "shippingInformation": "Free",
            "availabilityStatus": "In Stock",
            "returnPolicy": "30 days",
            "minimumOrderQuantity": 1,
        }
    ])

    result = add_record_hash(df)

    assert "record_hash" in result.columns
    assert len(result["record_hash"].iloc[0]) == 64


def test_same_record_generates_same_hash():
    df = pd.DataFrame([
        {
            "id": 1,
            "title": "Test Product",
            "description": "Test",
            "category": "test",
            "price": 100,
            "discountPercentage": 10,
            "rating": 4.5,
            "stock": 20,
            "brand": "Test",
            "sku": "TEST-001",
            "weight": 1,
            "width": 10,
            "height": 10,
            "depth": 10,
            "warrantyInformation": "1 year",
            "shippingInformation": "Free",
            "availabilityStatus": "In Stock",
            "returnPolicy": "30 days",
            "minimumOrderQuantity": 1,
        }
    ])

    result1 = add_record_hash(df)
    result2 = add_record_hash(df)

    assert (
        result1["record_hash"].iloc[0]
        == result2["record_hash"].iloc[0]
    )