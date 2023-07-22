
<h1 align="center">KopikatAPI 😺</h1>

<p align="center">👋 Hello, KopikatAPI 🐍 Python library for interacting with the Kopikat API. </p>

<p align="center">
  <a href="https://github.com/onuralpszr/kopikatAPI"><img src="https://raw.githubusercontent.com/onuralpszr/kopikatAPI/main/logo/kopikatAPI_Logo.png" alt="KopikatAPI"></a>
</p>

<p align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/onuralpszr/kopikatAPI">
  <img alt="Black" src="https://img.shields.io/badge/code%20style-black-black"/>
  <img alt="isort" src="https://img.shields.io/badge/isort-checked-yellow"/>
  <image alt="ruff" src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json"/>
</p>
<p align="center">
<a href="https://pypi.org/project/kopikatapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/kopikatapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/kopikatapi" target="_blank">
    <img src="https://img.shields.io/pypi/dm/kopikatapi?color=red" alt="Download Count">
</a>
<a href="https://pypi.org/project/kopikatapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/kopikatapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/kopikatapi" target="_blank">
    <img src="https://img.shields.io/pypi/status/kopikatapi?color=orange" alt="Project Status">
</a>
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

## Get your API Key

Contact with kopikat team from [here](https://kopikat.gitbook.io/api/quick-start#1.-get-your-api-key)


## Disclaimers
This is not an official Kopikat product. This is a personal project and is not affiliated with Kopikat in any way.
