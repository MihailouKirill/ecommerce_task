"""
Main ETL pipeline orchestration.
"""

import pandas as pd

from pipeline.ports.extractor import BaseExtractor
from pipeline.ports.loader import LoaderPort
from pipeline.ports.use_case import UseCasePort
from pipeline.transformers import (
    AggregateTransform,
    FinalTransformer,
    JoinTransformer,
    PurchasesTransformer,
    RevenueTransformer,
)


class SalesReportUseCase(UseCasePort):
    """
    Orchestrates the ETL pipeline to generate the sales report.

    This class acts as the core Use Case coordinator. It receives all necessary
    extractors and loaders via Dependency Injection, ensuring the business logic
    remains.
    """

    def __init__(
        self,
        events_extractor: BaseExtractor,
        products_extractor: BaseExtractor,
        customer_extractor: BaseExtractor,
        loader: LoaderPort,
    ):
        """
        Initialises the use case with required dependencies.

        Args:
            events_extractor: extractor for reading events data in batches.
            products_extractor: extractor for product reference data.
            customer_extractor: extractor for customer reference data.
            loader: loader for saving the finalized report.
        """
        self.events_extractor = events_extractor
        self.products_extractor = products_extractor
        self.customer_extractor = customer_extractor
        self.loader = loader

    def execute(self) -> None:
        """
        Executes the ETL pipeline.

        Steps performed:
            1. extracts static reference data into memory.
            2. initializes transformers (business rules).
            3. batch processing: reads events in batches and applies sequential transformations.
            4. final aggregation: concatenates chunks and applies final aggregations.
            5. load phase: persists the finalized report.
        """
        # 1. Load reference data
        products_df = pd.concat(self.products_extractor.extract(), ignore_index=True)
        customers_df = pd.concat(self.customer_extractor.extract(), ignore_index=True)

        # 2. Initialize business rules (Transformers)
        join_transformer = JoinTransformer(products_df, customers_df)
        purchases_transformer = PurchasesTransformer()
        revenue_transformer = RevenueTransformer()
        aggregate_transformer = AggregateTransform()
        final_transformer = FinalTransformer()

        # 3. Stream and process event batches
        events_df_generator = self.events_extractor.extract()
        all_batches = []

        for batch_df in events_df_generator:
            filtered_event = purchases_transformer(batch_df)
            joined_df = join_transformer(filtered_event)
            enriched_event = revenue_transformer(joined_df)
            transformed_df = aggregate_transformer(enriched_event)
            all_batches.append(transformed_df)

        # 4. Concatenate and perform final aggregation
        if not all_batches:
            return
        final_raw_df = pd.concat(all_batches, ignore_index=True)
        final_df = final_transformer(final_raw_df)

        # 5. Load Phase: Save the report
        self.loader.load(final_df)
