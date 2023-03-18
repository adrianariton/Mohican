# import the necessary packages
from imutils import build_montages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
from selenium import webdriver
from PIL import Image

def image_colorfulness(imageP):
    image = cv2.imread(imageP)
    # split the image into its respective RGB components
    (B, G, R) = cv2.split(image.astype("float"))
    # compute rg = R - G
    rg = np.absolute(R - G)
    # compute yb = 0.5 * (R + G) - B
    yb = np.absolute(0.5 * (R + G) - B)
    # compute the mean and standard deviation of both `rg` and `yb`
    (rbMean, rbStd) = (np.mean(rg), np.std(rg))
    (ybMean, ybStd) = (np.mean(yb), np.std(yb))
    # combine the mean and standard deviations
    stdRoot = np.sqrt((rbStd ** 2) + (ybStd ** 2))
    meanRoot = np.sqrt((rbMean ** 2) + (ybMean ** 2))
    # derive the "colorfulness" metric and return it
    return stdRoot + (0.3 * meanRoot)

def savePrint(imageFile, url):
    driver = webdriver.Chrome()
    driver.get(url)
    driver.get_screenshot_as_file(imageFile)

# 1 - Not colorful
# 2 - Slightly colorful
# 3 - Moderately colorful
# 4 - Averagely colorful
# 5 - Quite colorful
# 6 - Highly colorful
# 7 - Extremely colorful

# \sigma_{rgyb} = \sqrt{\sigma_{rg}^2 + \sigma_{yb}^2}
# \mu_{rgyb} = \sqrt{\mu_{rg}^2 + \mu_{yb}^2}
# C = \sigma_{rgyb} + 0.3 * \mu_{rgyb}

# 0 (min) - 150 (max) (valorile metricii)

def get_colorcoeff(url):
    '''
        0 - 10
    '''
    img = "img.png"
    savePrint(img, url)
    return image_colorfulness(img) / 16.0