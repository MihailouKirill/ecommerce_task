import pandas as pd
from numpy import nan
from pandas.testing import assert_frame_equal

from pipeline.adapters.transformers import (
    AggregateTransform,
    JoinTransformer,
    PurchasesTransformer,
    RevenueTransformer,
)


def test_revenue_transformer():
    df = pd.DataFrame({"quantity": [2, 10], "price": [0, 15]})
    expected_df = pd.DataFrame(
        {"quantity": [2, 10], "price": [0, 15], "total_revenue": [0, 150]}
    )

    transformer = RevenueTransformer()
    result = transformer.transform(df)

    assert_frame_equal(result, expected_df)


def test_revenue_transformer_empty():
    df = pd.DataFrame({})
    expected_df = pd.DataFrame({})

    transformer = RevenueTransformer()
    result = transformer.transform(df)

    assert_frame_equal(result, expected_df)


def test_join_transformer():

    fake_event_df = pd.DataFrame(
        {
            "quantity": [2, 10, 15],
            "product_id": [1, 2, 3],
            "customer_id": [2, 3, 4],
            "event_type": ["view_product", "purchase", "add_to_cart"],
        }
    )
    fake_product_df = pd.DataFrame(
        {
            "product_id": [1, 2, 3],
            "product_name": ["alpha", "beta", "gamma"],
            "category": ["Electronics", "Sport", "Garden"],
            "price": [10, 20, 30],
        }
    )
    fake_customer_df = pd.DataFrame(
        {"customer_id": [2, 3, 4], "segment": ["VIP", "New", "Regular"]}
    )

    expected_df = pd.DataFrame(
        {
            "quantity": [2, 10, 15],
            "product_id": [1, 2, 3],
            "customer_id": [2, 3, 4],
            "event_type": ["view_product", "purchase", "add_to_cart"],
            "product_name": ["alpha", "beta", "gamma"],
            "category": ["Electronics", "Sport", "Garden"],
            "price": [10, 20, 30],
            "segment": ["VIP", "New", "Regular"],
        }
    )

    transformer = JoinTransformer(fake_product_df, fake_customer_df)
    result = transformer.transform(fake_event_df)
    assert_frame_equal(result, expected_df)


def test_join_transformer_missing_data():
    fake_event_df = pd.DataFrame(
        {
            "quantity": [5],
            "product_id": [999],
            "customer_id": [999],
            "event_type": ["purchase"],
        }
    )
    fake_product_df = pd.DataFrame(
        {
            "product_id": [1],
            "product_name": ["alpha"],
            "category": ["Electronics"],
            "price": [10],
        }
    )
    fake_customer_df = pd.DataFrame({"customer_id": [2], "segment": ["New"]})

    expected_df = pd.DataFrame(
        {
            "quantity": [5],
            "product_id": [999],
            "customer_id": [999],
            "event_type": ["purchase"],
            "product_name": [nan],
            "category": [nan],
            "price": [nan],
            "segment": [nan],
        }
    )

    transformer = JoinTransformer(fake_product_df, fake_customer_df)
    result = transformer.transform(fake_event_df)
    # Dtypes might differ (object vs float64),check_dtype=False enforces value-only comparison
    assert_frame_equal(result, expected_df, check_dtype=False)


def test_purchases_transformer():
    df = pd.DataFrame(
        {
            "quantity": [2, 10, 15],
            "price": [0, 15, 20],
            "product_id": [1, 2, 3],
            "event_type": ["view_product", "purchase", "add_to_cart"],
        }
    )

    expected_df = pd.DataFrame(
        {"quantity": [10], "price": [15], "product_id": [2], "event_type": ["purchase"]}
    )

    transformer = PurchasesTransformer()
    result = transformer.transform(df)
    assert_frame_equal(result, expected_df)


def test_purchases_transformer_empty_data():
    df = pd.DataFrame(columns=["quantity", "price", "product_id", "event_type"])

    transformer = PurchasesTransformer()
    result = transformer.transform(df)
    assert result.empty
    assert list(result.columns) == ["quantity", "price", "product_id", "event_type"]


def test_aggregate_transformer():
    fake_df = pd.DataFrame(
        {
            "category": ["Electronics", "Electronics", "Garden"],
            "customer_segment": ["VIP", "VIP", "New"],
            "customer_id": [1, 1, 2],
            "quantity": [2, 3, 1],
            "total_revenue": [20, 200, 450],
        }
    )

    expected_df = pd.DataFrame(
        {
            "category": ["Electronics", "Garden"],
            "customer_segment": ["VIP", "New"],
            "total_revenue": [220, 450],
            "units_sold": [5, 1],
            "unique_customers": [1, 1],
        }
    )
    transformer = AggregateTransform()
    result = transformer.transform(fake_df)

    assert_frame_equal(result, expected_df)
