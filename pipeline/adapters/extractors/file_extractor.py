"""
File extraction adapter.
"""

import logging
from collections.abc import Generator

import pandas as pd

from pipeline.application.ports import IFileReaderPort
from pipeline.application.ports.batcher import IBatcherPort
from pipeline.application.ports.extractor import IBaseExtractorPort
from pipeline.application.ports.parser import IBaseParserPort

logger = logging.getLogger(__name__)


class FileExtractor(IBaseExtractorPort):
    """
    Reads data from files and yields it in batches as pandas DataFrames.
    Not tied to any specific source — works through ports only.
    """

    def __init__(
        self, opener: IFileReaderPort, parser: IBaseParserPort, batcher: IBatcherPort
    ) -> None:
        """
        Initializes the FileExtractor with required dependencies.

        Args:
            opener: Opens and yields file stream.
            parser: Parses file streams into DataFrames.
            batcher: Groups single DataFrames into batches.
        """
        self.opener = opener
        self.parser = parser
        self.batcher = batcher

    def extract(self) -> Generator[pd.DataFrame]:
        """
        Lazily reads files, parses their content, and yields data in batches.

        Yields:
            pd.DataFrame:a batched DataFrame ready for transformation.
        """
        logger.info("Starting file extraction stream...")
        single_dfs = (self.parser.parse(stream) for stream in self.opener.open())

        yield from self.batcher.batch(single_dfs)
