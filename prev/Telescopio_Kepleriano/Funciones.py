
#Numerical libraries
import numpy as np
import math
import time

#Image file handling
from PIL import Image

#Libraries for image interpolation
from scipy.interpolate import griddata
from scipy import interpolate

import pandas as pd


def interpolation (pixels, width_output, height_output, color):

  arry = np.zeros((width_output, height_output))
  for i in range(width_output):
    for j in range(height_output):
        if color == 'R':
            arry[i,j] = pixels[i,j][0]
        elif color == 'G':
            arry[i,j] = pixels[i,j][1]
        elif color == 'B':
            arry[i,j] = pixels[i,j][2]
    

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

    
  if color == 'R':
        for i in range(int_out.shape[0]):
            pixels[white_coords[i,0], white_coords[i,1] ] = ( int_out[i], 0, 0)
  elif color == 'G':
        for i in range(int_out.shape[0]):
            pixels[white_coords[i,0], white_coords[i,1] ] = ( 0, int_out[i], 0 )
  elif color == 'B':
        for i in range(int_out.shape[0]):
            pixels[white_coords[i,0], white_coords[i,1] ] = ( 0, 0, int_out[i] )
        



  #Returne pixels array with interpolated values
  return pixels

def ray_tracing_p(width, height, width_output, height_output, rayo, so, n1, obj, res, pixels, matriz, color, f_o, f_oc, a):
    si = (f_o*so)/(so-f_o)
    so2 = -(si-(f_o+f_oc))
    si2 = (f_oc*so2)/(so2-f_oc)
    
    LCA = 0

    # Iterate over each pixel of the image
    for i in range(width):
        for j in range(height):
            
            # Get pixel value and calculate its position relative to the center of the image
            pos_x = i
            pos_y = j
            pixel = obj.getpixel((pos_x, pos_y))
            x = pos_x - width/2
            y = pos_y - height/2

            # Calculate the distance from the particular pixel to the center of the object (in pixels)
            r = math.sqrt( x*x + y*y ) + 1 #Rounding correction

            #Input ray vector (point in the object plane)
            y_objeto = r*res # Conversion to real world coordinates

            

            
            

            # Define propagation matrices after and before the lens
            P2 = np.array([[1,0],[(si2)/n1,1]])
            P1 = np.array([[1,0],[(-so)/n1,1]])


            if rayo == 0: #principal
                alpha_entrada = math.atan(y_objeto/(so+5)) #This ray enters towards the center of the lens
            elif rayo == 1: #parallel
                alpha_entrada = 0 #This ray enters parallel to the optical axis
            V_entrada = np.array([n1*alpha_entrada,y_objeto])

            #Output ray vector calculation
            V_salida = P2.dot(matriz.dot(P1.dot(V_entrada)))

            #Transversal magnification
            y_imagen = V_salida[0]
            if rayo == 0: #principal
                Mt = (-1)*y_imagen/y_objeto #atan correction
            elif rayo == 1: #parallel
                Mt = y_imagen/y_objeto

            #Conversion from image coordinates to lens coordinates
            if a == 0:
                x_prime = Mt*0.25*x
                y_prime = Mt*0.25*y
            elif a == 1:
                x_prime = Mt*0.3*x
                y_prime = Mt*0.3*y
            pos_x_prime = int(x_prime + width_output/2)
            pos_y_prime = int(y_prime + height_output/2)

            if  pos_x_prime < 0 or pos_x_prime >= width_output:
                continue

            if  pos_y_prime < 0 or pos_y_prime >= height_output:
                continue
            
            if color == 'R':
                if rayo == 0: #principal
                    pixels[pos_x_prime, pos_y_prime] = (int(pixel), int(0), int(0))
                    next
                elif rayo == 1: #parallel
                    new_gray = (int(pixel) )
                    pix_fin = ( int(new_gray), int(0), int(0) )
                    pixels[pos_x_prime, pos_y_prime] = pix_fin

            elif color == 'G':
                if rayo == 0: #principal
                    pixels[pos_x_prime, pos_y_prime] = (int(0), int(pixel), int(0))
                    next
                elif rayo == 1: #parallel
                    new_gray = (int(pixel) )
                    pix_fin = ( int(0), int(new_gray), int(0) )
                    pixels[pos_x_prime, pos_y_prime] = pix_fin

            elif color == 'B':
                if rayo == 0: #principal
                    pixels[pos_x_prime, pos_y_prime] = (int(0), int(0), int(pixel))
                    next
                elif rayo == 1: #parallel
                    new_gray = (int(pixel))
                    pix_fin = ( int(0), int(0), int(new_gray) )
                    pixels[pos_x_prime, pos_y_prime] = pix_fin

    return pixels

def matriz_sistema(na, nb, nc, nd, ni, nr, R1, R2, R3, R4, R5, R6, da, db, dc, dd, di, dr):
    # Matrices de refraccion
    r1 = np.array([[1, 0] , [(-(na - 1)/R1), 1]])

    r2 = np.array([[1, 0] , [(-(nb - na)/R2), 1]])

    r3 = np.array([[1, 0] , [(-(nc - nb)/R3), 1]])

    r4 = np.array([[1, 0] , [(-(1 - nc)/R4), 1]])

    r5 = np.array([[1, 0] , [(-(nd - 1)/R5), 1]])

    r6 = np.array([[1, 0] , [(-(1 - nd)/R6), 1]])

    # Matrices de tralacion 

    T01 = np.array([[1, 1.3/nr] , [0, 1]])

    T12 = np.array([[1, da/na] , [0, 1]])

    T23 = np.array([[1, db/nb] , [0, 1]])

    T34 = np.array([[1, dc/nc] , [0, 1]])

    T45 = np.array([[1, di/ni] , [0, 1]])

    T56 = np.array([[1, dd/nd] , [0, 1]])

    T67 = np.array([[1, dr/nr] , [0, 1]])


    # Matriz de cada lente
    D = r6 @ T56 @ r5
    C = r4 @ T34 @ r3
    B = r3 @ T23 @ r2
    A = r2 @ T12 @ r1

    #Matriz del sistema
    M =  r6 @ T56 @ r5 @ T45 @ r4 @ T34 @ r3 @ T23 @ r2 @ T12 @ r1 

    return(M)

def focal(R1, R2, n, d):
    f = (n-1)*((1/R1)-(1/R2)+(((n-1)*d)/(n*R1*R2)))
    #f = 1/f
    return f

def get_constant():
    #Radios de curvatura

    
    R1 = 80.781569720954148552345414708949 
    R2 = -53.211336680402185240311271343552 
    R3 = 77.774183709363186996235338338139
    R4 =float('Inf')
    R5 = 10.2407
    R6 = -10.2407

    # Espesores 
    d_pk = 68.494469597779419052277427816432 
    d_kz = 6.4763126128800935613528323520288
    d_sf = 6.2322654
    d_K = 10
    d_i = 312
    d_r = 12

    n_i = 1
    n_r = 1


    

    return R1, R2, R3, R4, R5, R6, d_pk, d_kz, d_sf, d_K, d_i, d_r, n_i, n_r 

def image_sum(image1, image2, image3):
    max_width = max(image1.width, image2.width, image3.width)
    max_height = max(image1.height, image2.height, image3.height)

    image1 = image1.resize((max_width, max_height))
    image2 = image2.resize((max_width, max_height))
    image3 = image3.resize((max_width, max_height))

    output_image_3 = Image.new("RGB", (max_width, max_height))
    output_pixels_3 = output_image_3.load()

    for x in range(max_width):
        for y in range(max_height):
            r = image1.getpixel((x, y))[0] + image2.getpixel((x, y))[0] + image3.getpixel((x, y))[0]
            g = image1.getpixel((x, y))[1] + image2.getpixel((x, y))[1] + image3.getpixel((x, y))[1]
            b = image1.getpixel((x, y))[2] + image2.getpixel((x, y))[2] + image3.getpixel((x, y))[2]

            output_pixels_3[x, y] = (r, g, b)

    return output_image_3

def lens_type(lente):

    print("Seleccione el triplete que desea utilizar: \f")
    print(f"{lente.iloc[0:2, 0:1]}\f")

    t = int(input())
    
    if t == 0:
        n1 = lente.iloc[t,1]
        n2 = lente.iloc[t,2]
        n3 = lente.iloc[t,3]
        
    elif t == 1: 
        n1 = lente.iloc[t,1]
        n2 = lente.iloc[t,2]
        n3 = lente.iloc[t,3]
        print(n1,n2,n3)

    return t, n1,n2,n3

def planetas(planeta):
    print("Seleccione el planeta que desea observar\f")
    print(f"{planeta.iloc[0:4, 0:1]}\f")
    p = int(input()) 

    so = planeta.iloc[p,1]
    res = planeta.iloc[p,2]
    ruta = planeta.iloc[p,3]

    return so, res, ruta

def matriz_ideal(n1, n2, na, R1, R2, R3, R4, d1, d2, di, dr):

    r1 = np.array([[1, 0] , [(-(n1 - 1)/R1), 1]])

    r2 = np.array([[1, 0] , [(-(1 - n1)/R2), 1]])

    r3 = np.array([[1, 0] , [(-(n2 - 1)/R3), 1]])

    r4 = np.array([[1, 0] , [(-(1 - n2)/R4), 1]])


   
    T12 = np.array([[1, d1/n1] , [0, 1]])

    T23 = np.array([[1, di/na] , [0, 1]])

    T34 = np.array([[1, d2/n2] , [0, 1]])
    B = r4 @ T34 @ r3
    A = r2 @ T12 @ r1

    M = B @ T23 @ A
    return M