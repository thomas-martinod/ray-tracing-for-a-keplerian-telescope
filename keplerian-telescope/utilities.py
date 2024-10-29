import numpy as np
import math
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
from scipy.interpolate import griddata
from scipy import interpolate


# Function to read an image file from the disk
def imageRead(namefile):
    image = Image.open(namefile)
    return image

# Function to display an Image
def imageShow(image, title):
    plt.imshow(image), plt.title(title)
    # plt.axis('off')
    plt.show()


def interpolate_nan(array):
    # Create a grid of x and y coordinates
    x, y = np.indices(array.shape)
    
    # Get the valid (non-NaN) coordinates and values
    valid_mask = ~np.isnan(array)
    valid_x = x[valid_mask]
    valid_y = y[valid_mask]
    valid_values = array[valid_mask]
    
    # Interpolate over the NaN values
    interpolated_array = griddata(
        (valid_x, valid_y),  # points with known values
        valid_values,        # known values
        (x, y),              # points to interpolate
        method='cubic'       # interpolation method
    )
    
    # Fill remaining NaNs with 0s or another default value if any are left
    interpolated_array = np.nan_to_num(interpolated_array, nan=0)
    return interpolated_array