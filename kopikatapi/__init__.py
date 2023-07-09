"""KopikatAPI 🐍 Python library for interacting with the Kopikat API."""

import importlib.metadata as importlib_metadata

from .enums import Mode, Pipeline
from .kopikatapi import KopikatAPI

__version__ = importlib_metadata.version(__package__ or __name__)
__all__ = ["KopikatAPI", "Mode", "Pipeline"]
