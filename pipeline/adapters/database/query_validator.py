from pipeline.ports.query_validator import QueryValidatorPort


class SQLQueryValidator(QueryValidatorPort):
    """
    Validates that a SQL query is a non-empty and starts with SELECT.
    """

    @staticmethod
    def validate_query(query: str) -> str:
        """
        Validates and normalizes a SQL query.

        Args:
            query: SQL query

        Returns:
            stripped query(clean_query)
        """
        clean_query = query.strip()
        if not clean_query:
            raise ValueError("SQL cannot be empty")

        upper_query = clean_query.upper()
        if not (upper_query.startswith("SELECT")):
            raise ValueError(
                f"A read query (SELECT) was expected, but following was received:{query}"
            )

        return clean_query
