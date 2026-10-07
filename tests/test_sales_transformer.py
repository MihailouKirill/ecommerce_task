"""
Tests for domain layer transformers.

This module verifies that all business rules (filtering, joining, calculating,
and aggregating) are applied correctly to the pandas DataFrames.
"""

import pandas as pd
from numpy import nan
from pandas.testing import assert_frame_equal

from pipeline.transformers import (
    AggregateTransform,
    FinalTransformer,
    JoinTransformer,
    PurchasesTransformer,
    RevenueTransformer,
)


def test_revenue_transformer():
    """
    Tests that total revenue is correctly calculated as quantity * price.
    """

    df = pd.DataFrame({"quantity": [2, 10], "price": [0, 15]})
    expected_df = pd.DataFrame(
        {"quantity": [2, 10], "price": [0, 15], "total_revenue": [0, 150]}
    )

    transformer = RevenueTransformer()
    result = transformer(df)

    assert_frame_equal(result, expected_df)


def test_revenue_transformer_empty():
    """
    Tests that the revenue transformer handles an empty DataFrame without errors.
    """

    df = pd.DataFrame({})
    expected_df = pd.DataFrame({})

    transformer = RevenueTransformer()
    result = transformer(df)

    assert_frame_equal(result, expected_df)


def test_join_transformer():
    """
    Tests that event data is successfully enriched with product and customer dimensions.
    """
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
    result = transformer(fake_event_df)
    assert_frame_equal(result, expected_df)


def test_join_transformer_missing_data():
    """
    Tests that the join transformer handles missing reference data gracefully using left joins.
    """
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
    result = transformer(fake_event_df)
    # Dtypes might differ (object vs float64),check_dtype=False enforces value-only comparison
    assert_frame_equal(result, expected_df, check_dtype=False)


def test_purchases_transformer():
    """
    Tests that only 'purchase' events are retained in the DataFrame.
    """
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
    result = transformer(df)
    assert_frame_equal(result, expected_df)


def test_purchases_transformer_empty_data():
    """
    Tests that filtering an empty DataFrame returns an empty DataFrame with preserved columns.
    """
    df = pd.DataFrame(columns=["quantity", "price", "product_id", "event_type"])

    transformer = PurchasesTransformer()
    result = transformer(df)
    assert result.empty
    assert list(result.columns) == ["quantity", "price", "product_id", "event_type"]


def test_aggregate_transformer():
    """
    Tests the aggregation (grouping by category, segment, and customer).
    """
    fake_df = pd.DataFrame(
        {
            "category": ["Electronics", "Electronics", "Garden"],
            "segment": ["VIP", "VIP", "New"],
            "customer_id": [1, 1, 2],
            "quantity": [2, 3, 1],
            "total_revenue": [20, 200, 450],
        }
    )

    expected_df = pd.DataFrame(
        {
            "category": ["Electronics", "Garden"],
            "segment": ["VIP", "New"],
            "customer_id": [1, 2],
            "total_revenue": [220, 450],
            "units_sold": [5, 1],
        }
    )
    transformer = AggregateTransform()
    result = transformer(fake_df)

    assert_frame_equal(result, expected_df)


def test_final_transformer():
    """
    Tests the final aggregation, ensuring correct unique customer counts,
    revenue rounding, and column renaming.
    """
    fake_raw_df = pd.DataFrame(
        {
            "category": ["Electronics", "Electronics", "Electronics", "Books"],
            "segment": ["VIP", "VIP", "VIP", "New"],
            "customer_id": [1, 1, 2, 3],
            "total_revenue": [100.55, 50.11, 200.00, 30.00],
            "units_sold": [2, 1, 3, 1],
        }
    )
    expected_df = pd.DataFrame(
        {
            "category": ["Books", "Electronics"],
            "customer_segment": ["New", "VIP"],
            "total_revenue": [30.00, 350.66],
            "units_sold": [1, 6],
            "unique_customers": [1, 2],
        }
    )
    transformer = FinalTransformer()
    result = transformer(fake_raw_df)

    assert_frame_equal(result, expected_df)
