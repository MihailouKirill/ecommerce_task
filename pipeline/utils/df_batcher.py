from collections.abc import Generator, Iterable

import pandas as pd

from pipeline.interfaces.batchers_interfaces import BatcherPort


class DFBatcher(BatcherPort):
    """
    Groups individual pandas DataFrames into batches of size batch_size.
    """

    def __init__(self, batch_size:int)->None:
        """
        Initializes batcher.

        Args:
            batch_size: number of rows in each batch.
        """
        self.batch_size = batch_size

    def batch(
        self, items: Iterable[pd.DataFrame]
    ) -> Generator[pd.DataFrame]:
        """
        Takes a list of pandas DataFrames and batches them into batches of size batch_size.
        Args:
            items: An iterable stream of single DataFrames.

        Yields:
            pd.DataFrame: a batched DataFrame

        """
        bucket = []
        for item in items:
            bucket.append(item)

            if len(bucket) == self.batch_size:
                yield pd.concat(bucket, ignore_index=True)
                bucket.clear()

        if bucket:
            yield pd.concat(bucket, ignore_index=True)
