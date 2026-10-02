"""
Extracts data from a SQL query and loads into DataFrame
"""

import logging
from collections.abc import Generator

import pandas as pd

from pipeline.interfaces.database_interfaces import DataBaseConnection
from pipeline.interfaces.extractors_interfaces import BaseExtractor
from pipeline.utils import SQLQueryValidator

logger = logging.getLogger(__name__)


class DBExtractor(BaseExtractor):
    """
    Connects to a SQL query and loads into DataFrame
    """

    def __init__(
        self, db_manager: DataBaseConnection, query: str, batch_size: int
    ) -> None:
        self.db_manager = db_manager
        self.query = SQLQueryValidator.validate_query(query)
        self.batch_size = batch_size

    def extract(self) -> Generator[pd.DataFrame,None,None]:
        """
        Opens a connection to a SQL query and loads into DataFrame

        Yields:
            pd.DataFrame: A chunk of data from the SQL query

        """
        with self.db_manager as connection:
            try:
                chunks = pd.read_sql(self.query, connection, chunksize=self.batch_size)
                for chunk in chunks:
                    logger.info(f"Extracting batch : {chunk}")
                    yield chunk

            except Exception as e:
                logger.warning(f"{e}")
                raise
