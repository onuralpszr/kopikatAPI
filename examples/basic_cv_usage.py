# Sample use of kopikatapi

import cv2

from kopikatapi import KopikatAPI


def main():
    # initialize KopikatAPI
    api_key: str = "ENTER_YOUR_API_KEY"
    kopikatAPI = KopikatAPI(api_key)
    kopikatAPI.augment_image_file("bus_example.jpeg", "snow on the road")
    cv2.imshow("output", kopikatAPI.cv2_image())
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
