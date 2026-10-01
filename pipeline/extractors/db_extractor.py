"""
Extracts data from a SQL query and loads into DataFrame
"""

import logging

import pandas as pd

from pipeline.extractors.interfaces import BaseExtractor
from pipeline.utils import DataBaseConnection, SQLQueryValidator

logger = logging.getLogger(__name__)


class DBExtractor(BaseExtractor):
    """
    Connects to a SQL query and loads into DataFrame
    """

    def __init__(self, db_manager: DataBaseConnection, query: str) -> None:
        self.db_manager = db_manager
        self.query = SQLQueryValidator.validate_query(query)

    def extract(self) -> pd.DataFrame:
        """
        Opens a connection to a SQL query and loads into DataFrame

        Returns:
            df: dataframe with data from SQL query

        """
        with self.db_manager as connection:
            try:
                df = pd.read_sql(self.query, connection)
                logger.info(f"{df.shape}")
            except Exception as e:
                logger.warning(f"{e}")
                raise

        return df
