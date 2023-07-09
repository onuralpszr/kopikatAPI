from enum import Enum


class Mode(Enum):
    DEFAULT = "default"
    HIGH_PRESERVED = "high-preserved"


class Pipeline(Enum):
    DEFAULT = "default"
    CUSTOMIZED = "customized"


class ImageType(Enum):
    JPEG = "image/jpeg"
    JPG = "image/jpeg"
    PNG = "image/png"
