from typing import IO

import pandas as pd

from pipeline.interfaces.parsers_interfaces import BaseParser


class PandasJsonParser(BaseParser):
    """
    Adapter for parsing JSON file streams into pandas DataFrames
    """

    def parse(self, file_stream: IO) -> pd.DataFrame:
        """
        Reads a JSON byte stream and converts it into a DataFrame

        Args:
            file_stream: An opened file stream containing JSON data

        Returns:
            pd.DataFrame: Parsed data
        """
        return pd.read_json(file_stream)
