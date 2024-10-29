# -*- coding: utf-8 -*-
"""
Title: biconvex lens

Description: Python script that performs a ray tracing simulation of an object through a biconvex lens, given certain parameters such as the object distance, focal distance, and refractive index.
The code imports the necessary libraries such as numpy and PIL, and defines a function ray_tracing that performs the simulation for a given ray (either principal or parallel) and generates an output image file in PNG format.
The main steps of the code involve computing the power and lens matrix of the biconvex lens, calculating the input and output ray vectors, finding the transversal magnification, and converting the image coordinates to lens coordinates.
The code also loads an input image file (default case: "saturn.jpg"), creates a new output image file, and calls the ray_tracing function twice, once for the principal ray and once for the parallel ray, to generate the final output image.

Created on Mon Sep 23 - 2019
Modified on  March 17th - 2024

@author: Carlos Trujillo (catrujilla@eafit.edu.co), Universidad EAFIT (original version)
@author: Raul Castaneda (racastaneq@eafit.edu.co) Universidad EAFIT (last version)

"""

# import libraries
import numpy as np
import math
from PIL import Image
from scipy.interpolate import griddata
from scipy import interpolate


def interpolation (pixels, width_output, height_output):
  arry = np.zeros((width_output, height_output))
  for i in range(width_output):
    for j in range(height_output):
      arry[i,j] = pixels[i,j][0]

  # Get the coordinates of the non-white pixels
  nonwhite_coords = np.argwhere(arry != 255)
  # Get the coordinates of the white pixels
  white_coords = np.argwhere(arry == 255)

  # Get the pixel values of the non-white pixels
  nonwhite_pixels = arry[nonwhite_coords[:,0], nonwhite_coords[:,1]]

  # Interpolate the pixel values of the white pixels
  interpolated_pixels = griddata(nonwhite_coords, nonwhite_pixels, white_coords, method='linear', rescale=True)

  #Change resulting NaN values with some value (zero, for instance)
  interpolated_pixels = np.nan_to_num(interpolated_pixels, nan=127.0)

  #Round interpolated values to integers
  int_out = np.round(interpolated_pixels).astype(int)

  #Fill white pixels locations with interpolated values
  for i in range(int_out.shape[0]):
    pixels[white_coords[i,0], white_coords[i,1] ] = ( int_out[i], int_out[i], int_out[i] )

  #Returne pixels array with interpolated values
  return pixels


def lens_matrix(n1, n2, R1, R2, dl):
    # inputs:
    # n1 - medium refractive index
    # n2 - Lens refractive index
    # R1 - Radius R1
    # R2 - Radius R2

    # dl -

    # Power of each interface
    D1 = (n2 - n1) / R1
    D2 = (n2 - n1) / (-R2)

    # Lens matrix
    a1 = (1 - (D2 * dl) / n2)
    a2 = -D1 - D2 + (D1 * D2 * dl / n2)
    a3 = dl / n2
    a4 = (1 - (D1 * dl) / n2)
    lensMatrix = np.array([[a1, a2], [a3, a4]])

    return lensMatrix


def ray_tracing(object, width, height, magni, objDist, imaDist, n1, n2, R1, R2, dl, res, aberration, pixels):

    width_output = int(width*(abs(magni)))
    height_output = int(height*(abs(magni)))

    # first propagation (before lens)
    firstPro = np.array([[1, 0], [-objDist / n1, 1]])

    # matrix lens
    lensMatrix = lens_matrix(n1, n2, R1, R2, dl)

    # second propagation (after lens)
    secondPro = np.array([[1, 0], [imaDist / n1, 1]])

    alpha_entrada = 0  # This ray enters parallel to the optical axis

    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):
            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j
            pixel = object.getpixel((pos_x, pos_y))
            x = pos_x - width / 2
            y = pos_y - height / 2

            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt(x * x + y * y) + 1  # Rounding correction

            # Input ray vector (point in the object plane)
            y_objeto = r * res  # Conversion to real world coordinates
            v_input = np.array([n1 * alpha_entrada, y_objeto])
            v_output = np.dot(firstPro, v_input)
            v_output = np.dot(lensMatrix, v_output)
            v_output = np.dot(secondPro, v_output)

            y_imagen = v_output[1]
            Mt = y_imagen / y_objeto
            # Conversion from image coordinates to lens coordinates
            x_prime = Mt * x
            y_prime = Mt * y
            pos_x_prime = int(x_prime + width_output / 2)
            pos_y_prime = int(y_prime + height_output / 2)

            new_gray = (int(pixel) + pixels[pos_x_prime, pos_y_prime][0]) / 2
            pix_fin = (int(new_gray), int(new_gray), int(new_gray))
            pixels[pos_x_prime, pos_y_prime] = pix_fin

    return pixels


def biconvex(object, R1, R2, n1, n2, dl, objDist):
    # inputs:
    # object - image
    # R1 - Radius R1
    # R2 - Radius R2
    # n1 - medium refractive index
    # n2 - Lens refractive index
    # dl -
    # objDist - object distance from vertex of the biconvex lens
    width, height = object.size
    print("Object image dimensions: ", width, "X ", height)
    # focal distance
    f = R1 * R2 / ((R2 - R1) * (n2 - n1))
    print("focal length: ", f)

    # image distance
    imaDist = (f * objDist) / (objDist - f)
    print("image Distance: ", imaDist)

    # magnification
    magni = -imaDist/objDist
    print ("Mt: ", magni)

    # Pixel size to real world size conversion
    res = 0.0001

    aberration = True
    #CREAR UNAFUNCION QUE P ERMITA INTROUCIR UN TIPO DE ABERRACIÓN#

    width_output = int(width*(abs(magni)))
    height_output = int(height*(abs(magni)))

    # Create new Image and a Pixel Map
    image = Image.new("RGB", (width_output, height_output), "white")
    pixels = image.load()

    # Compute image with parallel ray
    pixels = ray_tracing(object, width, height, magni, objDist, imaDist, n1, n2, R1, R2, dl, res, aberration, pixels)


    interpolation(pixels, width_output, height_output)
    print("Interpolation performed")


    #print(np.array(pixels))
    #Save Images to File
    image.save('output_C.png', format='PNG')

    return