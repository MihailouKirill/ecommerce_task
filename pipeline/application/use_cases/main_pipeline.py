"""
Main ETL pipeline orchestration.
"""

import logging

import pandas as pd

from pipeline.application.ports.compactor import ICompactorPort
from pipeline.application.ports.extractor import IBaseExtractorPort
from pipeline.application.ports.loader import ILoaderPort
from pipeline.application.ports.use_case import IUseCasePort
from pipeline.domain.transformers import (
    AggregateTransform,
    JoinTransformer,
    PurchasesTransformer,
    RevenueTransformer,
)

logger = logging.getLogger(__name__)


class SalesReportUseCase(IUseCasePort):
    """
    Orchestrates the ETL pipeline to generate the sales report.

    This class acts as the core Use Case coordinator. It receives all necessary
    extractors and loaders via Dependency Injection, ensuring the business logic
    remains.
    """

    def __init__(
        self,
        events_extractor: IBaseExtractorPort,
        products_extractor: IBaseExtractorPort,
        customer_extractor: IBaseExtractorPort,
        loader: ILoaderPort,
        compactor: ICompactorPort,
    ):
        """
        Initialises the use case with required dependencies.

        Args:
            events_extractor: extractor for reading events data in batches.
            products_extractor: extractor for product reference data.
            customer_extractor: extractor for customer reference data.
            loader: loader for saving the finalized report.
            compactor: Compactor for post-processing the final report CSV.
        """
        self.events_extractor = events_extractor
        self.products_extractor = products_extractor
        self.customer_extractor = customer_extractor
        self.loader = loader
        self.compactor = compactor

    def execute(self) -> None:
        """
        Executes the ETL pipeline.

        Steps performed:
            1. Extracts static reference data into memory.
            2. Initializes transformers.
            3. Batch processing: reads events in batches and applies sequential transformations.
            4. Loads each finalized batch into the report
            5. Compacts the report.
        """
        # 1. Load reference data
        logger.info("Loading reference data from database...")
        try:
            products_df = pd.concat(
                self.products_extractor.extract(), ignore_index=True
            )
            customers_df = pd.concat(
                self.customer_extractor.extract(), ignore_index=True
            )
            logger.info(
                "Reference data loaded: %d products and %d customers.",
                len(products_df),
                len(customers_df),
            )
        except Exception:
            logger.exception("Failed to load reference data from database.")
            raise

        # 2. Initialize Transformers
        join_transformer = JoinTransformer(products_df, customers_df)
        purchases_transformer = PurchasesTransformer()
        revenue_transformer = RevenueTransformer()
        aggregate_transformer = AggregateTransform()
        # 3. Stream and process event batches
        events_df_generator = self.events_extractor.extract()

        batch_idx = 0
        # 4. Loads each finalized batch into the report
        try:
            for batch_df in events_df_generator:
                batch_idx += 1
                raw_count = len(batch_df)
                filtered_event = purchases_transformer(batch_df)
                del batch_df
                if filtered_event.empty:
                    logger.debug(
                        "Batch #%d: 0 purchases out of %d events (skipped).",
                        batch_idx,
                        raw_count,
                    )
                    continue

                joined_df = join_transformer(filtered_event)
                enriched_event = revenue_transformer(joined_df)
                del filtered_event

                aggregated_batch = aggregate_transformer(enriched_event)
                del enriched_event

                self.loader.load(aggregated_batch)
                del aggregated_batch
        finally:
            # 5. Compacts the report.
            self.compactor.compact()

        logger.info("Event processing completed: %d batches processed.", batch_idx)
