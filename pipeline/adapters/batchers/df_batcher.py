from collections.abc import Generator, Iterable

import pandas as pd

from pipeline.ports.batcher import BatcherPort


class DFBatcher(BatcherPort):
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
        Takes a iterable of  DataFrames and batches them.

        Args:
            items: An iterable stream of single DataFrames.

        Yields:
            pd.DataFrame:A concatenated batched DataFrame.
        """
        bucket = []
        for item in items:
            bucket.append(item)

            if len(bucket) == self.batch_size:
                yield pd.concat(bucket, ignore_index=True)
                bucket.clear()

        if bucket:
            yield pd.concat(bucket, ignore_index=True)
