import logging
import zipfile
from collections.abc import Iterator
from io import BytesIO
from pathlib import Path
from typing import IO

from pipeline.application.ports import IFileReaderPort

logger = logging.getLogger(__name__)


class ZipOpener(IFileReaderPort):
    """
    Handles navigation through nested ZIP archives.
    """

    def __init__(self, path: Path) -> None:
        """
        Initializes the ZipOpener with the target directory path.

        Args:
            path : Path to the directory containing outer ZIP archives.
        """
        self.path = path

    def open(self) -> Iterator[IO]:
        """
        Processes nested ZIP archives and returns streams of the target files.

        Yields:
            IO: An opened byte stream of the target file inside the zip archive.
        """
        zip_files = list(self.path.glob("*.zip"))
        if not zip_files:
            logger.warning("No ZIP archive found in %s", self.path.resolve())
            return
        # 1 Find all ZIP archives in the current directory
        for zip_file_path in zip_files:
            logger.info("Opening archive: %s", zip_file_path.name)
            try:
                with zipfile.ZipFile(zip_file_path) as outer_zip:
                    # 2 Iterate over inner archives
                    for inner_item in outer_zip.namelist():
                        with outer_zip.open(inner_item) as inner_zip_file:
                            # Load the inner ZIP bytes into memory (BytesIO).
                            # This creates a "virtual file" that the zipfile module can read.
                            virtual_file = BytesIO(inner_zip_file.read())

                            with zipfile.ZipFile(virtual_file) as inner_zip:
                                # 3 Iterate over JSONs files
                                for target_file_name in inner_zip.namelist():
                                    # 4 Open the target file and yield the stream to the parser
                                    with inner_zip.open(
                                        target_file_name
                                    ) as opened_file:
                                        yield opened_file
            except zipfile.BadZipFile:
                logger.error(f"Corrupted archive detected: {zip_file_path}")
                raise
            except Exception:
                logger.exception(f"Unexpected error while reading {zip_file_path}")
                raise
