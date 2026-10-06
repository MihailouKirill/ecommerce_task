"""
Database extraction adapter.
"""

import logging
from collections.abc import Generator

import pandas as pd

from pipeline.ports.database_connection import DataBaseConnection
from pipeline.ports.extractor import BaseExtractor

logger = logging.getLogger(__name__)


class DBExtractor(BaseExtractor):
    """
    Extracts data from a database by executing a SQL query.
    """

    def __init__(
        self, db_manager: DataBaseConnection, query: str, batch_size: int
    ) -> None:
        """
        Initializes the database extractor.
        
        Args:
            db_manager: context manager for  db connection.
            query: SQL query to execute.
            batch_size: Size of each batch.
        """
        self.db_manager = db_manager
        self.query = query  # SQLQueryValidator.validate_query(query)
        self.batch_size = batch_size

    def extract(self) -> Generator[pd.DataFrame]:
        """
        Executes the query and yields results in batches.

        Yields:
            pd.DataFrame: A chunk of data from the database.

        """
        with self.db_manager as connection:
            try:
                chunks = pd.read_sql(self.query, connection, chunksize=self.batch_size)
                for chunk in chunks:
                    logger.info(f"Extracting batch : {chunk}")
                    yield chunk

            except Exception as e:
                logger.exception(f"{e}")
                raise
