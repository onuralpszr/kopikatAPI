from base64 import b64decode
from io import BytesIO

from cv2 import IMREAD_COLOR
from cv2 import imdecode as cv2_imdecode
from numpy import frombuffer, ndarray
from numpy import uint8 as npuint8
from PIL import Image
from PIL.Image import Image as PIL_Image
from requests import Response as requests_Response
from requests import post as requests_post

from kopikatapi.enums import ImageType, Mode, Pipeline


class KopikatAPI:
    def __init__(
        self,
        api_key: str,
        strength: float = 0.0,
        mode: Mode = Mode.DEFAULT,
        pipeline: Pipeline = Pipeline.DEFAULT,
    ) -> None:
        self.__api_key: str = api_key
        self.__mode: Mode = mode
        self.__pipeline: Pipeline = pipeline
        self.__response: dict = {}
        self.__strength: float = strength

    def augment_image_file(self, image_path: str, environment: str) -> dict:
        image = open(image_path, "rb")
        if image is None:
            raise ValueError("Image is missing")

        imgread = image.read()
        pil_img = Image.open(BytesIO(imgread))
        return self.__augment_image_pil(imgread, pil_img, environment)

    def __augment_image_pil(
        self, img_byte: bytes, pil_image: PIL_Image, environment: str
    ) -> dict:
        # Convert PIL image to byte
        image_enum_type = ImageType.PNG
        # Check if image is valid for JPEG, JPG, PNG and set image type
        if (pil_image.format == "JPEG") or (pil_image.format == "JPG"):
            image_enum_type = ImageType.JPEG
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
            url, params=params, headers=headers, files=files
        )

        if response.status_code == 200:
            self.__response = response.json()
            return self.__response
        elif response.status_code == 401:
            raise ValueError("API key is invalid")
        elif response.status_code == 422:
            raise ValueError(f"Validation Error: {response.json()['detail']}")
        elif response.status_code == 400:
            raise ValueError(f"Bad Request: {response.json()['detail']}")
        elif response.status_code == 500:
            raise ValueError("Internal Server Error, please try again later")
        else:
            raise ValueError(f"Unknown Error, status code: {response.status_code}")

    @property
    def strength(self) -> float:
        return self.__strength

    @strength.setter
    def strength(self, strength: float) -> None:
        if strength < 0.0 or strength > 1.0:
            raise ValueError("Strength must be between 0.0 and 1.0")
        self.__strength = strength

    @property
    def pipeline(self) -> Pipeline:
        return self.__pipeline

    @pipeline.setter
    def pipeline(self, pipeline: Pipeline) -> None:
        self.__pipeline = pipeline

    @property
    def mode(self) -> Mode:
        return self.__mode

    @mode.setter
    def mode(self, mode: Mode) -> None:
        self.__mode = mode

    def get_b64image(self) -> bytes:
        b64image: str = self.__response["b64image"]
        print(b64image)
        image_data: bytes = b64decode(b64image)
        return image_data

    def cv2_image(self) -> ndarray:
        image_data: bytes = self.get_b64image()
        nparr: ndarray = frombuffer(image_data, npuint8)
        img: ndarray = cv2_imdecode(nparr, IMREAD_COLOR)
        return img

    def numpy_image(self) -> ndarray:
        image_data: bytes = self.get_b64image()
        return frombuffer(image_data, npuint8)

    def save_image(self, filename: str) -> None:
        image_data: bytes = self.get_b64image()
        with open(f"{filename}.jpg", "wb") as f:
            f.write(image_data)
