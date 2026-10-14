import logging
from collections.abc import Callable, Iterable
from pathlib import Path

import pandas as pd

from pipeline.application.ports import ICompactorPort

logger = logging.getLogger(__name__)


class CSVReportCompactor(ICompactorPort):
    """
    Adapter responsible for post-processing and consolidating accumulated CSV report files.
    """

    def __init__(
        self,
        file_path: Path,
        final_transformer: Callable[[Iterable[pd.DataFrame]], pd.DataFrame],
        chunk_size: int,
    ) -> None:
        """
        Initializes the CSV report compactor.

        Args:
            file_path: Path to the CSV report file to be compacted.
            final_transformer: Callable that lazily consumes DataFrame chunks and
                returns the final aggregated report.
            chunk_size: Number of rows read from the CSV file per chunk.
        """
        self.file_path = file_path
        self.final_transformer = final_transformer
        self.chunk_size = chunk_size

    def compact(self) -> None:
        """
        Reads the accumulated CSV in chunks, aggregates it with the final
        transformer and atomically replaces the file with the result.
        """
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            logger.info("Nothing to compact: %s is missing or empty", self.file_path)
            return

        logger.info(
            "Starting compaction for %s (chunk size: %d)",
            self.file_path,
            self.chunk_size,
        )

        with pd.read_csv(self.file_path, chunksize=self.chunk_size) as reader:
            final_df = self.final_transformer(reader)

        if final_df.empty:
            logger.warning(
                "Final report is empty, leaving %s untouched", self.file_path
            )
            return

        tmp = self.file_path.with_suffix(".tmp.csv")
        final_df.to_csv(tmp, index=False)
        tmp.replace(self.file_path)
        logger.info("Report compacted into %d rows: %s", len(final_df), self.file_path)
