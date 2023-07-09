"""KopikatAPI 🐍 Python library for interacting with the Kopikat API."""

from base64 import b64decode
from io import BytesIO

from cv2 import IMREAD_COLOR
from cv2 import imdecode as cv2_imdecode
from numpy import frombuffer, ndarray
from numpy import uint8 as npuint8
from PIL import Image
from PIL.Image import Image as PIL_Image
from requests import Response as requests_Response
from requests import codes as requests_codes
from requests import post as requests_post

from kopikatapi.enums import ImageType, Mode, Pipeline


class KopikatAPI:
    """KopikatAPI class for image augmentation using Kopikat API."""

    def __init__(
        self,
        api_key: str,
        strength: float = 0.0,
        mode: Mode = Mode.DEFAULT,
        pipeline: Pipeline = Pipeline.DEFAULT,
    ) -> None:
        """Initialize KopikatAPI class.

        KokipatAPI class for image augmentation using Kopikat API

        Args:
            api_key (str): API key for Kopikat API
            strength (float, optional): Strength of augmentation. Defaults to 0.0.
            mode (Mode, optional): Mode of augmentation. Defaults to Mode.DEFAULT.
            pipeline (Pipeline, optional): Pipeline of augmentation.
                Defaults to Pipeline.DEFAULT.

        Raises:
            ValueError: If API key is missing

        """
        self.__api_key: str = api_key
        self.__mode: Mode = mode
        self.__pipeline: Pipeline = pipeline
        self.__response: dict = {}
        self.__strength: float = strength

    def augment_image_file(self, image_path: str, environment: str) -> dict:
        """Augment image from file.

        Args:
            image_path (str): Path to image file
            environment (str): Prompt for augmentation

        Returns:
            dict: Response from Kopikat API
        """
        image = open(image_path, "rb")
        if image is None:
            raise ValueError("Image is missing")

        imgread = image.read()
        pil_img = Image.open(BytesIO(imgread))
        return self.__augment_image_pil(imgread, pil_img, environment)

    def __augment_image_pil(
        self, img_byte: bytes, pil_image: PIL_Image, environment: str
    ) -> dict:
        """Augment image from PIL image object.

        Args:
            img_byte (bytes): Image in bytes
            pil_image (PIL_Image): PIL image object
            environment (str): Prompt for augmentation

        Returns:
            dict: Response from Kopikat API

        """
        # Convert PIL image to byte
        image_enum_type = ImageType.PNG
        # Check if image is valid for JPEG, JPG, PNG and set image type
        if (pil_image.format == "JPEG") or (pil_image.format == "JPG"):
            image_enum_type = ImageType.JPG
        elif pil_image.format == "PNG":
            image_enum_type = ImageType.PNG
        else:
            raise ValueError("Invalid image")

        return self.__augment_image(
            img_byte=img_byte,
            environment=environment,
            image_type=pil_image.format.lower(),
            image_enum_type=image_enum_type,
        )

    def __augment_image(
        self,
        img_byte: bytes,
        environment: str,
        image_type: str,
        image_enum_type: ImageType,
    ) -> dict:
        """Augment image from bytes.

        Args:
            img_byte (bytes): Image in bytes
            environment (str): Prompt for augmentation
            image_type (str): Image type
            image_enum_type (ImageType): Image type enum


        """
        if not self.__api_key:
            raise ValueError("API key is missing")
        url: str = "http://api.kopikat.co/augment"
        params = {
            "key": self.__api_key,
            "environment": environment,
            "pipeline": self.__pipeline.value,
            "mode": self.__mode.value,
        }
        headers = {"accept": "application/json"}
        files = {"image": (f"input.{image_type}", img_byte, image_enum_type.value)}
        if self.__pipeline == Pipeline.CUSTOMIZED:
            params["strength"] = self.__strength

        response: requests_Response = requests_post(
            url, params=params, headers=headers, files=files, timeout=60
        )

        if response.status_code == requests_codes["ok"]:
            self.__response = response.json()
            return self.__response
        elif response.status_code == requests_codes["unauthorized"]:
            raise ValueError("API key is invalid")
        elif response.status_code == requests_codes["unprocessable_entity"]:
            raise ValueError(f"Validation Error: {response.json()['detail']}")
        elif response.status_code == requests_codes["bad_request"]:
            raise ValueError(f"Bad Request: {response.json()['detail']}")
        elif response.status_code == requests_codes["internal_server_error"]:
            raise ValueError("Internal Server Error, please try again later")
        else:
            raise ValueError(f"Unknown Error, status code: {response.status_code}")

    @property
    def strength(self) -> float:
        """Strength of augmentation."""
        return self.__strength

    @strength.setter
    def strength(self, strength: float) -> None:
        """Strength of augmentation."""
        if strength < 0.0 or strength > 1.0:  # noqa: PLR2004
            raise ValueError("Strength must be between 0.0 and 1.0")
        self.__strength = strength

    @property
    def pipeline(self) -> Pipeline:
        """Pipeline of augmentation."""
        return self.__pipeline

    @pipeline.setter
    def pipeline(self, pipeline: Pipeline) -> None:
        """Pipeline of augmentation."""
        self.__pipeline = pipeline

    @property
    def mode(self) -> Mode:
        """Mode of augmentation."""
        return self.__mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        """Mode of augmentation."""
        self.__mode = mode

    def get_b64image(self) -> bytes:
        """Get base64 image from response."""
        b64image: str = self.__response["b64image"]
        image_data: bytes = b64decode(b64image)
        return image_data

    def cv2_image(self) -> ndarray:
        """Get OpenCV image from response."""
        image_data: bytes = self.get_b64image()
        nparr: ndarray = frombuffer(image_data, npuint8)
        img: ndarray = cv2_imdecode(nparr, IMREAD_COLOR)
        return img

    def numpy_image(self) -> ndarray:
        """Get Numpy image from response."""
        image_data: bytes = self.get_b64image()
        return frombuffer(image_data, npuint8)

    def save_image(self, filename: str) -> None:
        """Save image from response."""
        image_data: bytes = self.get_b64image()
        with open(f"{filename}.jpg", "wb") as f:
            f.write(image_data)
