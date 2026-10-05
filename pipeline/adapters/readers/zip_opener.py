import zipfile
from collections.abc import Iterator
from io import BytesIO
from pathlib import Path
from typing import IO

from pipeline.ports.readers import FileReaderPort


class ZipOpener(FileReaderPort):
    """
    Handles navigation through nested ZIP archives.
    """

    def __init__(self, path: Path) -> None:
        """
        Initializes the ZipOpener with the target directory path.

        Args:
            path (Path): Path to the directory containing outer ZIP archives.
        """
        self.path = path

    def open(self) -> Iterator[IO]:
        """
        Yields:
            IO: An opened byte stream of the target file inside the zip archive
        """
        # 1 Find all ZIP archives in the current directory
        for zip_file_path in self.path.glob("*.zip"):
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
                                with inner_zip.open(target_file_name) as opened_file:
                                    yield opened_file
