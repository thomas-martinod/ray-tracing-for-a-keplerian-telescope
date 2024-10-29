import matrix_calculator as mc
import utilities as ut
from data import get_data


import numpy as np
import math
from PIL import Image

def format_image(path):
    img = ut.imageRead(path)
    blue, green, red = img.split()
    # ut.imageShow(blue, 'blue channel')
    # ut.imageShow(green,'green channel')
    # ut.imageShow(red, 'red channel')
    return blue, green, red



def keplerian_ray_tracing(object, width_output, height_output, color, n_air=1.0003, aberration=False):
    width, height = object.size

    # Load lens data and matrices
    objective_lens, eyepiece_lens, rgb, refraction_crown = get_data()
    M_system = mc.simple_system(n_in=refraction_crown[color], n_out=n_air, objective=objective_lens, eyepiece=eyepiece_lens)

    # Define the initial angle for ray input
    alpha_entrada = 0

    # Create a new grayscale Image and Pixel Map for each color channel
    image = Image.new("L", (width_output, height_output), "white")
    pixels = image.load()

    # Iterate over each pixel of the input image
    for pos_x in range(width):
        for pos_y in range(height):
            # Get pixel and calculate relative position to the center
            pixel = object.getpixel((pos_x, pos_y))
            x = pos_x - width / 2
            y = pos_y - height / 2

            # Calculate distance from center and angle theta
            r = math.sqrt(x * x + y * y) + 1  # Avoid zero radius issues
            theta = math.atan2(y, x)  # Angle from the center to (x, y)

            # Input vector (angle and distance to object in real-world units)
            y_objeto = r
            v_input = np.array([alpha_entrada, y_objeto])

            # Apply transformations for ray tracing
            v_output = np.dot(M_system.T, v_input)
            r_prime = v_output[1]

            # Coordinate transformation to output image space
            pos_x_prime = int(r_prime * math.cos(theta) + width_output / 2)
            pos_y_prime = int(r_prime * math.sin(theta) + height_output / 2)

            # Check bounds before setting pixel to avoid errors
            if 0 <= pos_x_prime < width_output and 0 <= pos_y_prime < height_output:
                pixels[pos_x_prime, pos_y_prime] = pixel

    return image, pixels


def main():
    obj, eye, rgb, refraction = get_data()

    object = ut.imageRead("keplerian-telescope/figs/Full_Moon.jpg")
    magni = 5

    width, height = object.size

    width_output = int(width*(abs(magni)))
    height_output = int(height*(abs(magni)))

    red, green, blue = object.split()

    # Create new Image and a Pixel Map
    image = Image.new("RGB", (height_output, height_output), "white")
    pixels = image.load()

    # Process each color channel through ray tracing, applying magnification and inversion
    b, bp = keplerian_ray_tracing(blue, width_output, height_output, "B", n_air=1.0003, aberration=False)
    r, rp = keplerian_ray_tracing(red, width_output, height_output, "R",  n_air=1.0003, aberration=False)
    g, gp = keplerian_ray_tracing(green, width_output, height_output, "G", n_air=1.0003, aberration=False)


    # Convierte cada canal a escala de grises antes de fusionarlos
    r_gray = r.convert("L")
    g_gray = g.convert("L")
    b_gray = b.convert("L")

    r_array = np.array(r_gray, dtype=float)
    g_array = np.array(g_gray, dtype=float)
    b_array = np.array(b_gray, dtype=float)

    # Replace white spaces with NaN (assuming 255 as white space, change if different)
    r_array[r_array == 255] = np.nan
    g_array[g_array == 255] = np.nan
    b_array[b_array == 255] = np.nan

    # Apply interpolation to each grayscale channel
    r_filled = ut.interpolate_nan(r_array)
    g_filled = ut.interpolate_nan(g_array)
    b_filled = ut.interpolate_nan(b_array)


    # Convert to image
    r_image = Image.fromarray(r_filled.astype(np.uint8))
    g_image = Image.fromarray(g_filled.astype(np.uint8))
    b_image = Image.fromarray(b_filled.astype(np.uint8))
    
    # Fusiona los canales de nuevo en una imagen RGB
    IMAGENSOTA = Image.merge("RGB", (r_image, g_image, b_image))

    # Muestra la imagen procesada
    ut.imageShow(IMAGENSOTA, 'Processed Jupiter Image')




main()