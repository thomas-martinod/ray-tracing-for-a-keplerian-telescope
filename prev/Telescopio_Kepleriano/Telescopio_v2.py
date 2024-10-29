import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from Funciones import *

interpolate = True
lente = pd.read_json('Lentes.json')
planeta = pd.read_json('Planetas.json')
RGB_ref = ['R' ,'G', 'B']
f_tot_RGB = []
matrices_RGB = []
Mt_RGB = []
width_output_RGB = []
height_output_RGB = []
output_images = []
output_pixels_RGB = [] 


CHIEF_RAY = 0
PARALLEL_RAY = 1
Aumento = 2

Lente = pd.read_json('Lentes.json')
planeta = pd.read_json('Planetas.json')

#so, res, ruta = planetas(planeta)


so = 360

res =  0.3# Cada píxel equivale a res

#n1, n2, n3, n4 = lens_type(Lente)

def interpolation_2 (pixels):

  arry = np.zeros((width_output_RGB, height_output_RGB))
  for i in range(width_output_RGB):
    for j in range(height_output_RGB):
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
    pixels[white_coords[i,0], white_coords[i,1] ] = ( int_out[i] ,int_out[i],int_out[i])

  #Returne pixels array with interpolated values
  return pixels

n1 = [1.5278, 1.5303, 1.5348]            #n_pk
n2 = [1.611771, 1.616370, 1.626022]      #n_kz      
n3 = [1.6963, 1.7040, 1.7209]            #n_sf
n4 = [1.5101, 1.5130, 1.5188]             #n_K


R1, R2, R3, R4, R5, R6, d_pk, d_kz, d_sf, d_K, d_i, d_r, n_i, n_r = get_constant()

Imagen = Image.open('C:Imaging\Full_Moon.jpg') #Menu

red, green, blue = Imagen.split()
RGB = [red, green, blue ]
width, height = Imagen.size

width_new, height_new = width*Aumento, height*Aumento

width_output_RGB = (int(width*(abs(Aumento))))
height_output_RGB = (int(height*(abs(Aumento))))
Imagen_resize = Imagen.resize((width_new,height_new))

print('')
for i in range(3):
    matriz = matriz_sistema(n1[i], n2[i], n3[i], n4[i], n_i, n_r, R1, R2, R3, R4, R5, R6, d_pk, d_kz, d_sf, d_K, d_i, d_r)
   # print('Matriz de transformacion para {}'.format(RGB_ref[i]))
   # print(matriz)
    matrices_RGB.append(matriz)
    Mt_RGB.append(Aumento)

    output_images.append(Image.new("RGB", (width_output_RGB, height_output_RGB)))
    output_pixels_RGB.append(output_images[i].load())

    output_pixels_RGB[i] = ray_tracing_p(width, height, width_output_RGB, height_output_RGB, CHIEF_RAY, so, 1, RGB[i], res, output_pixels_RGB[i], Mt_RGB[i], matrices_RGB[i], RGB_ref[i])
    output_pixels_RGB[i] = ray_tracing_p(width, height, width_output_RGB, height_output_RGB, PARALLEL_RAY, so, 1, RGB[i], res, output_pixels_RGB[i], Mt_RGB[i], matrices_RGB[i], RGB_ref[i]) 
 

    if interpolate:
        output_pixels_RGB[i] = interpolation(output_pixels_RGB[i], width_output_RGB, height_output_RGB, RGB_ref[i])
        print("se hizo interpolacion para {}".format(RGB_ref[i]))
    pass
    print('')

imagen_final = image_sum(output_images[0], output_images[1], output_images[2])

#output_images[0].save('output.png', format='PNG')

fig, (ax3, ax4, ax5) = plt.subplots(1, 3, figsize=(15, 5))

'''
ax1.imshow(output_images[0])
ax1.set_title('Red Channel')
ax1.axis('off')

ax2.imshow(output_images[1])
ax2.set_title('Green Channel')
ax2.axis('off')
'''
ax3.imshow(output_images[0])
ax3.set_title('Blue Channel')
ax3.axis('off')

ax4.imshow(imagen_final)
ax4.set_title('Imagen original\n maginficada')
ax4.axis('off')

ax5.imshow(Imagen_resize)
ax5.set_title('Imagen final')
ax5.axis('off')



plt.show()

