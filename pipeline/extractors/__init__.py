"""
Extracts data from SQL query & from zip files

Creates a class that connects to the PostgreSQL database and loads table into DataFrame, and
{in_the_future} Creates a class that can navigate the nested zip structure and loads all
events into a single Pandas DataFrame.
"""

from .db_extractor import *
from .interfaces import *
