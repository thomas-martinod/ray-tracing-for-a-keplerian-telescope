import cv2
import numpy as np
import utilities as ut

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import griddata
import os
from data import get_data, get_aberration_data
import matrix_calculator as mc
import math


def chromatic_aberration_score(image):
    # Convert to grayscale for each color channel
    red_channel = image[:, :, 2]
    green_channel = image[:, :, 1]
    blue_channel = image[:, :, 0]

    # Detect edges for each color channel using Canny edge detector
    edges_red = cv2.Canny(red_channel, 100, 200)
    edges_green = cv2.Canny(green_channel, 100, 200)
    edges_blue = cv2.Canny(blue_channel, 100, 200)

    # Calculate the shift in pixels between edge positions of color channels
    shift_rg = np.sum(np.abs(edges_red - edges_green))
    shift_rb = np.sum(np.abs(edges_red - edges_blue))
    shift_gb = np.sum(np.abs(edges_green - edges_blue))

    # Average the shifts as the chromatic aberration score
    chromatic_aberration_score = (shift_rg + shift_rb + shift_gb) / 3.0

    return chromatic_aberration_score


img = ut.imageRead("keplerian-telescope/img_with_aberrations/Earth.jpg")

chromatic_aberration_score(img)