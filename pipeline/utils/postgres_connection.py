import logging
from types import TracebackType
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

from pipeline.config import Settings
from pipeline.utils.interfaces import DataBaseConnection

logger = logging.getLogger(__name__)


class DataBasePostgreSQLConnection(DataBaseConnection):
    """
    Creating  context manager for connecting to the Docker PostgreSQL database

    This Class takes the settings parameters , and manages the database
    connection lifecycle (connects on enter , close on exit)

    Args:
        settings_param(Settings): Database settings passed from the config file
    """

    def __init__(self, settings_param: Settings) -> None:
        self.db_url = (
            f"postgresql+psycopg2://{settings_param.db_user}:"
            f"{settings_param.db_password}@{settings_param.db_host}:"
            f"{settings_param.db_port}/{settings_param.db_name}"
        )
        self.engine: Engine = create_engine(self.db_url)
        self.connection: Any = None

    def __enter__(self) -> Connection:
        """
        Establishes the database connection and creates

        Returns:
            connection: Connection to the database
        """
        self.connection = self.engine.connect()

        logger.info("Successfully connected to Database")

        return self.connection

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Correctly close the connection to the database

        Args:
            exc_type: type of exception
            exc_val: copy of exception
            exc_tb: contains info about  the call stack
        """
        try:
            if exc_type is None:
                logger.info("Commiting transaction")
                self.connection.commit()
            else:
                logger.warning(
                    f"Error something wrong with connection :{exc_type.__name__}"
                )
                self.connection.rollback()
        finally:
            self.connection.close()
