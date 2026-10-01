"""
Package for creating a context manager for the database connection

This package consists of interfaces.py - location of an abstract class DataBaseConnection
&  postgres_connection.py - context manager for connecting to postgresql database +
query_validator that validates SQL query
"""

from .interfaces import *
from .postgres_connection import *
from .query_validator import *
