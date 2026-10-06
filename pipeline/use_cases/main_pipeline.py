"""
Main ETL pipeline orchestration.
"""
from pipeline.adapters.database import DataBasePostgreSQLConnection, SQLQueryValidator
from pipeline.config import app_settings
from pipeline.adapters.extractors import DBExtractor,FileExtractor
from pipeline.adapters.readers import ZipOpener
from pipeline.adapters.parsers import PandasJsonParser
from pipeline.adapters.batchers import DFBatcher
from pipeline.adapters.transformers import JoinTransformer ,PurchasesTransformer, RevenueTransformer, AggregateTransform
from pipeline.adapters.loaders import FileLoader

from pathlib import Path
import pandas as pd
def run_pipeline():
    """
        Executes the complete ETL pipeline for sales data.

        Extracts dimensions from DB, processes event batches lazily,
        performs  aggregation, and loads the final report.
        """
    db_connection = DataBasePostgreSQLConnection(app_settings)
    validator = SQLQueryValidator()

    products_data_from_db = DBExtractor(
            db_connection,
            validator.validate_query("SELECT * FROM products"),
            app_settings.batch_size
        )

    customers_data_from_db = DBExtractor(
            db_connection,
            validator.validate_query("SELECT * FROM customers"),
            app_settings.batch_size
        )

    products_df = pd.concat(products_data_from_db.extract(),ignore_index=True)
    customers_df = pd.concat(customers_data_from_db.extract(),ignore_index=True)

    zip_opener = ZipOpener(path=Path(__file__).resolve().parents[2]/"data")
    json_parser = PandasJsonParser()
    batcher =DFBatcher(app_settings.batch_size)

    events_data_from_file = FileExtractor(
            zip_opener,
            json_parser,
            batcher
        )
    join_transformer = JoinTransformer(products_df,customers_df)
    purchases_transformer=PurchasesTransformer()
    revenue_transformer = RevenueTransformer()
    aggregate_transformer = AggregateTransform()

    events_df_generator = events_data_from_file.extract()

    all_batches=[]
    for batch_df in events_df_generator:
        filtered_event = purchases_transformer.transform(batch_df)
        joined_df = join_transformer.transform(filtered_event)
        enriched_event = revenue_transformer.transform(joined_df)
        transformed_df = aggregate_transformer.transform(enriched_event)
        all_batches.append(transformed_df)

    final_raw_df = pd.concat(all_batches,ignore_index=True)

    final_df = final_raw_df.groupby(
        ["category", "segment"],as_index=False).agg(
        total_revenue=("total_revenue", "sum"),
        units_sold=("units_sold", "sum"),
        unique_customers=("customer_id", "nunique")
    )

    final_df = final_df.rename(columns={"segment": "customer_segment"})
    final_df["total_revenue"] = final_df["total_revenue"].round(2)
    final_df["units_sold"]=final_df["units_sold"].astype(int)
    final_df = final_df

    FileLoader(Path('reports/sales_report.csv')).load(final_df)

