"""
Extracts data from nested zip files and load all events into a single Pandas DataFrame..
"""

from collections.abc import Generator

import pandas as pd

from pipeline.ports.batcher import BatcherPort
from pipeline.ports.extractor import BaseExtractor
from pipeline.ports.parser import BaseParser
from pipeline.ports.readers import FileReaderPort


class FileExtractor(BaseExtractor):
    """
    Reads data from files and yields it in batches as pandas DataFrames.
    Not tied to any specific source — works through ports only.
    """

    def __init__(
        self, opener: FileReaderPort, parser: BaseParser, batcher: BatcherPort
    ) -> None:
        """
        Initializes the FileExtractor with required dependencies.

        Args:
            opener: Opens and yield file stream
            parser: Parses file streams into DataFrames
            batcher: Groups single DataFrames into batches
        """
        self.opener = opener
        self.parser = parser
        self.batcher = batcher

    def extract(self) -> Generator[pd.DataFrame]:
        """
        Lazily reads files, parses their content, and yields data in batches

        Yields:
            pd.DataFrame:a batched DataFrame ready for loading
        """
        single_dfs = (self.parser.parse(stream) for stream in self.opener.open())

        yield from self.batcher.batch(single_dfs)
