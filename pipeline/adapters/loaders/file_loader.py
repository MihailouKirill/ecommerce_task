import logging
from pathlib import Path

import pandas as pd

from pipeline.application.ports.loader import ILoaderPort

logger = logging.getLogger(__name__)


class FileLoader(ILoaderPort):
    """
    Adapter for saving a DataFrame to CSV file.
    """

    def __init__(self, output_path: Path) -> None:
        """
        Initialize the FileLoader.

        Args:
            output_path: the file path to save the DataFrame.
        """
        self.output_path = output_path
        self._is_first_batch = True

    def load(self, data: pd.DataFrame) -> None:
        """
        Saves a DataFrame batch. Overwrites the file on the first batch,
        and appends without headers on all subsequent batches.

        Args:
            data:DataFrame batch  to save.
        """
        # Ensure the target directory exists (e.g. `reports/`).
        if data.empty:
            logger.debug("Received empty DataFrame, skipping write")
            return

        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        if self._is_first_batch:
            data.to_csv(self.output_path, mode="w", index=False, header=True)
            self._is_first_batch = False
            logger.info(
                "Created output report at %s (%d rows written)",
                self.output_path,
                len(data),
            )
        else:
            data.to_csv(self.output_path, mode="a", index=False, header=False)
            logger.debug(f"Appended {len(data)} rows to {self.output_path.name}")
