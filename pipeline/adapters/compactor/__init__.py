"""
Compactor adapters.

Provides implementations for post-processing and consolidating accumulated batch reports.
"""

from .csv_compactor import CSVReportCompactor

__all__: list[str] = ["CSVReportCompactor"]
