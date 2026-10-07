"""
Tests for the FileExtractor adapter.

Uses dependency injection with fake objects (Stubs/Mocks) to test the
extraction logic independently from the actual file system.
"""

from collections.abc import Generator, Iterable, Iterator
from io import BytesIO
from typing import IO

import pandas as pd
import pytest

from pipeline.adapters.extractors import FileExtractor
from pipeline.ports import BaseParser, BatcherPort, FileReaderPort


class FakeOpener(FileReaderPort):
    """
    Fake file opener that yields byte streams.
    """

    def open(self) -> Iterator[IO]:
        yield BytesIO(b"Fake data1")
        yield BytesIO(b"Fake data2")
        yield BytesIO(b"Fake data3")


class FakeParser(BaseParser):
    """
    Fake parser that returns a predefined DataFrame.
    """

    def parse(self, file_stream: IO) -> pd.DataFrame:
        return pd.DataFrame({"col1": [1, 2]})


class FakeBatcher(BatcherPort):
    """
    Fake batcher that groups DataFrames based on a batch size.
    """

    def __init__(self, batch_size: int) -> None:
        self.batch_size = batch_size

    def batch(self, items: Iterable[pd.DataFrame]) -> Generator[pd.DataFrame]:
        bucket = []
        for item in items:
            bucket.append(item)

            if len(bucket) == self.batch_size:
                yield pd.concat(bucket, ignore_index=True)
                bucket.clear()

        if bucket:
            yield pd.concat(bucket, ignore_index=True)


class BrokenFakeParser(BaseParser):
    """
    Fake parser simulating a failure during file parsing.
    """

    def parse(self, file_stream: IO) -> pd.DataFrame:
        raise ValueError("File is broken")


def test_file_extractor_success() -> None:
    """
    Tests that the FileExtractor correctly coordinates opening, parsing,
    and batching without throwing errors.
    """
    fake_parser = FakeParser()
    fake_batcher = FakeBatcher(batch_size=2)
    fake_opener = FakeOpener()

    test_extractor = FileExtractor(fake_opener, fake_parser, fake_batcher)

    result_batches = list(test_extractor.extract())

    assert len(result_batches) == 2
    assert isinstance(result_batches[0], pd.DataFrame), (
        "First element needs to be a pd.DataFrame"
    )


def test_file_extractor_failure() -> None:
    """
    Tests that the FileExtractor raises an error if the parser fails.
    """
    fake_parser = BrokenFakeParser()
    fake_batcher = FakeBatcher(batch_size=2)
    fake_opener = FakeOpener()

    test_extractor = FileExtractor(fake_opener, fake_parser, fake_batcher)
    with pytest.raises(ValueError) as exc_info:
        list(test_extractor.extract())

    assert "File is broken" in str(exc_info.value)
