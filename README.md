
<h1 align="center">KopikatAPI 😺</h1>

<p align="center">👋 Hello, KopikatAPI 🐍 Python library for interacting with the Kopikat API. </p>

<p align="center">
  <a href="https://github.com/onuralpszr/kopikatAPI"><img src="https://raw.githubusercontent.com/onuralpszr/kopikatAPI/main/logo/kopikatAPI_Logo.png" alt="KopikatAPI"></a>
</p>

Kopikat project allows people to generative data augmentation. So people can enlarge and diversify datasets and is specifically helpful for datasets with up to 5,000 images that are typical for real-life AI projects.

## 💻 Installation

You can install the `KopikatAPI` library using pip in between [Python**3.11>=Python>=3.8**](https://www.python.org/) environment.

```bash
pip install kopikatapi
```

## 🔥 Quickstart

```python

from kopikatapi import KopikatAPI
import cv2

api_key: str = 'ENTER YOUR API KEY HERE'
kopikatAPI = KopikatAPI(api_key)
kopikatAPI.augment_image_file('image.png', 'summer time')
cv2.imshow("output",kopikatAPI.cv2_image())
cv2.waitKey(0)

```


## Disclaimers
This is not an official Kopikat product. This is a personal project and is not affiliated with Kopikat in any way.
