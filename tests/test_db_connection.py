"""
Module for testing the PostgreSQL connection adapter.

Ensures that the context manager correctly handles commits on success
and rollbacks on failure.
"""

from unittest.mock import MagicMock, patch

import pytest

from pipeline.adapters.database.postgres_connection import DataBasePostgreSQLConnection


@pytest.fixture
def fake_settings() -> MagicMock:
    """
    Сreates a fake settings object.

    Returns:
        MagicMock: Fake object settings for testing
    """
    settings = MagicMock()
    settings.db_host = "test"
    settings.db_port = 1341
    settings.db_user = "test"
    settings.db_password = "test"
    settings.db_name = "test"
    return settings


@patch("pipeline.adapters.database.postgres_connection.create_engine")
def test_success_connection(
    mock_create_engine: MagicMock, fake_settings: MagicMock
) -> None:
    """
    Tests that a successful transaction commits and closes the connection.

    Args:
        mock_create_engine(MagicMock):Mocked SQLAlchemy create_engine function
        fake_settings(MagicMock): Fake object settings for testing
    """
    mock_conn = MagicMock()
    mock_engine = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = mock_conn

    with DataBasePostgreSQLConnection(fake_settings) as connection:
        connection.execute("SELECT * FROM products LIMIT 5")

    mock_conn.commit.assert_called_once()
    mock_conn.rollback.assert_not_called()
    mock_conn.close.assert_called_once()


@patch("pipeline.adapters.database.postgres_connection.create_engine")
def test_failure_connection(
    mock_create_engine: MagicMock, fake_settings: MagicMock
) -> None:
    """
    Tests that an exception inside the CM triggers a rollback.

    Args:
        mock_create_engine(MagicMock):Mocked SQLAlchemy create_engine function
        fake_settings(MagicMock): Fake object settings for testing
    """
    mock_conn = MagicMock()
    mock_engine = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = mock_conn
    with pytest.raises(ValueError), DataBasePostgreSQLConnection(fake_settings):
        raise ValueError

    mock_conn.commit.assert_not_called()
    mock_conn.rollback.assert_called_once()
    mock_conn.close.assert_called_once()
