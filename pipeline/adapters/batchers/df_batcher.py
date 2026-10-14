import logging
from collections.abc import Generator, Iterable
from itertools import batched

import pandas as pd

from pipeline.application.ports.batcher import IBatcherPort

logger = logging.getLogger(__name__)


class DFBatcher(IBatcherPort[pd.DataFrame]):
    """
    Groups individual pandas DataFrames into batches of size batch_size.
    """

    def __init__(self, batch_size: int) -> None:
        """
        Initializes  the batcher.

        Args:
            batch_size:Number of DataFrames to accumulate before concatenating.
        """
        self.batch_size = batch_size

    def batch(self, items: Iterable[pd.DataFrame]) -> Generator[pd.DataFrame]:
        """
        Takes an iterable of  DataFrames and batches them.

        Args:
            items: An iterable stream of single DataFrames.

        Yields:
            pd.DataFrame:A concatenated batched DataFrame.
        """
        for batch in batched(items, self.batch_size):
            merged = pd.concat(batch, ignore_index=True)
            logger.debug(
                "Batched %d DataFrames into single chunk of %d rows",
                len(batch),
                len(merged),
            )
            del batch
            yield merged
            del merged
