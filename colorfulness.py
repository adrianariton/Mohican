
# import the necessary packages
import re
import requests
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from selenium import webdriver
from PIL import Image

def num_of_images(url):
    response = requests.get(url)
    # print(response.text)
    # Find all image tags in the HTML content
    img_tags = re.findall("<img.*>", response.text)
    # print(img_tags)

    # Filter the image tags to only those with valid image file extensions
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif"]
    valid_img_tags = [tag for tag in img_tags if any(ext in tag.lower() for ext in valid_extensions)]

    # Count the number of valid image tags
    num_images = len(valid_img_tags)

    print(f"There are {num_images} images on {url}")
    return num_images

def image_colorfulness(imageP):
    image = cv2.imread(imageP)
    (B, G, R) = cv2.split(image.astype("float"))
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    return stdRoot + (0.3 * meanRoot)

def savePrint(imageFile, url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.get_screenshot_as_file(imageFile)

def get_category(url):
    img = "aux.png"
    savePrint(img, url)
    coef = image_colorfulness(img)

    if coef <= 50:
        return "not-colorful"

    if coef <= 100:
        number_of_images = num_of_images(url)
        if number_of_images < 5:
            return "simplistic_none"
        return "simplistic_images"

    return "complex"

if __name__ == "__main__":
    # example
    url = "https://www.pbinfo.ro"
    url1 = "http://www.compjour.org/warmups/govt-text-releases/intro-to-bs4-lxml-parsing-wh-press-briefings/"
    url2 = "https://pbinfo.ro"
    url3 = "https://www.geeksforgeeks.org/python-split-dictionary-keys-and-values-into-separate-lists/"
    url4 = "https://github.com/"
    url5 = "https://www.innovationlabs.ro/"
    url6 = "https://eestec.ro"
    url7 = "https://www.hrs-bg.com/"
    url8 = "https://www.vodafone.ro/"
    print(get_category(url6))