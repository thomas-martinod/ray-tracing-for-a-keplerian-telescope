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
from PIL import Image
import matplotlib.pyplot as plt
import biconvexLens as bcl

image = Image.open("codigos-raul/saturn.jpg")
plt.imshow(image)
plt.title('Object')
plt.show()

# Biconvex Lens parameters, the sign follows the - Sign Convention for Lenses
# all units in cm
R1 = 0.2
R2 = -0.2
dl = 0.01
n1 = 1
n2 = 1.5

# object distance
objDist = 0.11

output = bcl.biconvex(image, R1, R2, n1, n2, dl, objDist)
print(output)