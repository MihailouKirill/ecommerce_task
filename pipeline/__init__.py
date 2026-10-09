"""
Project main ETL pipeline package

This package orchestrates the ETL pipeline, consists of :
"Extractor" Component Package, "Transformer" Component Package,
"Loader" Component Package, Shared, non-core utilities, and config
"""

from .config import Settings, app_settings

__all__: list[str] = ["Settings", "app_settings"]
