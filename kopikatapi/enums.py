"""Enum functions for Kopikat API."""
from enum import Enum


class Mode(Enum):
    """Enum for mode types."""

    DEFAULT = "default"
    HIGH_PRESERVED = "high-preserved"


class Pipeline(Enum):
    """Enum for pipeline types."""

    DEFAULT = "default"
    CUSTOMIZED = "customized"


class ImageType(Enum):
    """Enum for image types."""

    JPG = "image/jpeg"
    PNG = "image/png"
