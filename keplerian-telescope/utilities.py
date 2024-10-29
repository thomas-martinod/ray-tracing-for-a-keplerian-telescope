import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from scipy.interpolate import griddata
import os
from data import get_data, get_aberration_data
import matrix_calculator as mc
import math

def imageRead(namefile):
    image = Image.open(namefile)
    return image

def imageShow(images, titles):
    num_images = len(images)
    
    fig, axs = plt.subplots(1, num_images, figsize=(5*num_images, 5))

    for i in range(num_images):
        axs[i].imshow(images[i])
        axs[i].set_title(titles[i])
        axs[i].axis('on')

    plt.tight_layout()
    plt.show()

def imageSave(image, choice, corrected = False):
    save_directory = "keplerian-telescope/img_with_aberrations/"
    if corrected == True:
        save_directory = "keplerian-telescope/img_no_aberrations/"
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)
    save_path = os.path.join(save_directory, f"{choice}.jpg")

    image.save(save_path)
    print(f"Image saved with aberrations at {save_path}")

def format_image(path):
    img = imageRead(path)
    blue, green, red = img.split()
    return blue, green, red


def interpolate_nan(array):
    x, y = np.indices(array.shape)
    
    valid_mask = ~np.isnan(array)
    valid_x = x[valid_mask]
    valid_y = y[valid_mask]
    valid_values = array[valid_mask]
    
    interpolated_array = griddata(
        (valid_x, valid_y),
        valid_values,
        (x, y),
        method='cubic'
    )
    
    interpolated_array = np.nan_to_num(interpolated_array, nan=0)
    return interpolated_array

def ray_tracing(object, width_output, height_output, M_system):
    width, height = object.size
    alpha_entrada = 0

    image = Image.new("L", (width_output, height_output), "white")
    pixels = image.load()

    for pos_x in range(width):
        for pos_y in range(height):
            pixel = object.getpixel((pos_x, pos_y))
            x = pos_x - width / 2
            y = pos_y - height / 2

            r = math.sqrt(x * x + y * y) + 1
            theta = math.atan2(y, x)

            y_objeto = r
            v_input = np.array([alpha_entrada, y_objeto])

            v_output = np.dot(M_system, v_input)
            r_prime = v_output[1]

            pos_x_prime = int(r_prime * math.cos(theta) + width_output / 2)
            pos_y_prime = int(r_prime * math.sin(theta) + height_output / 2)

            if 0 <= pos_x_prime < width_output and 0 <= pos_y_prime < height_output:
                pixels[pos_x_prime, pos_y_prime] = pixel

    return image

def keplerian_ray_tracing(object, width_output, height_output, color, n_air=1.0003):
    objective_lens, eyepiece_lens, _ , refraction_NBK7 = get_data()
    M_system = mc.simple_system(n_in=refraction_NBK7[color], n_out=n_air, objective=objective_lens, eyepiece=eyepiece_lens)
    img = ray_tracing(object, width_output, height_output, M_system)
    return img


def correct_aberration(object, width_output, height_output, color, n_air=1.0003):
    refraction_NPK51_1, refraction_NKZFS4_1,refraction_SF15_1, refraction_NPK51_2, refraction_NKZFS4_2, refraction_SF15_2  = get_aberration_data()
    M_system = mc.aberration_system(refraction_NPK51_1, refraction_NKZFS4_1,refraction_SF15_1, refraction_NPK51_2, refraction_NKZFS4_2, refraction_SF15_2, n_air, color)
    img = ray_tracing(object, width_output, height_output, M_system)
    return img

