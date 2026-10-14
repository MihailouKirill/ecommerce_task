import logging
from types import TracebackType

from sqlalchemy import create_engine
from sqlalchemy.engine import Connection, Engine

from pipeline.application.ports import IDataBaseConnectionPort

logger = logging.getLogger(__name__)


class DataBasePostgreSQLConnection(IDataBaseConnectionPort):
    """
    Creates  context manager for connecting to the Docker's PostgreSQL database.

    This Class takes the settings parameters , and manages the database
    connection lifecycle (connects on enter , close on exit).
    Guarantees that the connection is properly closed on exiting the
    `with` block, even if an exception occurs inside it.

    Args:
        settings_param(Settings): Database settings passed from the config file.
    """

    def __init__(
        self, db_host: str, db_port: int, db_user: str, db_password: str, db_name: str
    ) -> None:
        self.db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine: Engine = create_engine(self.db_url)
        self.connection: Connection | None = None

    def __enter__(self) -> Connection:
        """
        Establishes the database connection and creates.

        Returns:
            connection: Connection to the database.
        """
        self.connection = self.engine.connect()

        logger.info("Successfully connected to PostgreSQL Database")
        return self.connection

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        Correctly close the connection to the database.

        Args:
            exc_type: type of exception.
            exc_val: copy of exception.
            exc_tb: contains info about  the call stack.
        """
        if self.connection is not None:
            try:
                if exc_type is None:
                    logger.debug("Commiting transaction")
                    self.connection.commit()
                else:
                    logger.warning(
                        "Error occurred during DB transaction (%s), rolling back",
                        exc_type.__name__,
                    )
                    self.connection.rollback()
            finally:
                self.connection.close()
                logger.info("Closed PostgreSQL Database connection")
