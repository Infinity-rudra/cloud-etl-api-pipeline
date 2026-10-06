import pandas as pd

from src.transformation.transform import transform_data


def test_transformation_removes_unnecessary_columns(
    tmp_path
):

    input_file = tmp_path / "input.csv"

    df = pd.DataFrame(
        {
            "id": [1],
            "title": ["Test Product"],
            "price": [100],
            "stock": [20],
            "thumbnail": ["image.jpg"],
            "images": ["image1.jpg,image2.jpg"]
        }
    )

    df.to_csv(
        input_file,
        index=False
    )

    result = transform_data(
        str(input_file)
    )

    assert "thumbnail" not in result.columns
    assert "images" not in result.columns

    assert "id" in result.columns
    assert "title" in result.columns
    assert "price" in result.columns
    assert "stock" in result.columns