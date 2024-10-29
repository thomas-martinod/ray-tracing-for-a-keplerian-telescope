import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import griddata

import os


def imageRead(namefile):
    image = Image.open(namefile)
    return image

def imageShow(images, titles):
    num_images = len(images)
    
    fig, axs = plt.subplots(1, num_images, figsize=(5*num_images, 5))

    # Display each image in its subplot
    for i in range(num_images):
        axs[i].imshow(images[i])
        axs[i].set_title(titles[i])
        axs[i].axis('off')  # Hide the axis

    plt.tight_layout()  # Adjust layout to prevent overlap
    plt.show()

def imageSave(image, choice):
    save_directory = "keplerian-telescope/img_with_aberrations/"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    save_path = os.path.join(save_directory, f"{choice}.jpg")

    image.save(save_path)
    print(f"Image saved with aberrations at {save_path}")



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

def correct_aberration():
    pass