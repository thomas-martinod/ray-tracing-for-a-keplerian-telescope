import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
from Funciones import *

lente = pd.read_json('Lentes.json')
planeta = pd.read_json('Planetas.json')
RGB_ref = ['R' ,'G', 'B']
f_tot_RGB = []
matrices_RGB = []
matrices_a = []
Ma_a = []
Ma_RGB = []
width_output_RGB = []
height_output_RGB = []
output_images = []
output_pixels_RGB = [] 
focales = []
focales_a = []
focales_k = []
focales_k_a = []
width_outputs = []
height_outputs = []
width_outputs_a = []
height_outputs_a = []

CHIEF_RAY = 0
PARALLEL_RAY = 1
atenuacion = 15
interpolate = True

#variable deffinition----------------------------------------------------------------------------------------------------------------------------------------

#triplet
n1 = [1.5278, 1.5303, 1.5348]            #n_pk
n2 = [1.611771, 1.616370, 1.626022]      #n_kz      
n3 = [1.6963, 1.7040, 1.7209]            #n_sf
n4 = [1.5101, 1.5120, 1.5128]            #n_K

R1_a = 432.74085224252796633184224524504
R2_a = -432.74085224252796633184224524504



so, res, ruta = planetas(planeta)
R1, R2, R3, R4, R5, R6, d_pk, d_kz, d_sf, d_K, d_i, d_r, n_i, n_r = get_constant()

obj = Image.open(ruta)
obj_2 = Image.open(ruta)
width, height = obj.size
r, g, b = obj.split()
r_a, g_a, b_a = obj_2.split()
RGB = [r,g,b]
RGB_a = [r_a, g_a, b_a]

print('')
#Core--------------------------------------------------------------------------------------------------------------------------------------------

for channel in range(3):
    f_pk = focal(R1, R2, n1[channel], d_pk)
    f_kz = focal(R2, R3, n2[channel], d_kz)
    f_sf = focal(R3, R4, n3[channel], d_sf)
    f_K = focal(R5, R6, n4[channel], d_K)
    f_K_a = focal(10, 15, n4[channel], d_K)
    focales.append(1/(f_pk + f_kz + f_sf))
    focales_k.append(f_K)
    focales_k_a.append(f_K_a)

    print('focal del triplete para {} = {}'.format(RGB_ref[channel],focales[channel]))
    print('focal del ocular  para {} = {}\n'.format(RGB_ref[channel], 1/f_K))

    f_kz_a = focal(R1_a, R2_a, n2[channel], d_K)
    focales_a.append(1/f_kz_a)
   # print(focales_a[channel])


    matriz_RGB = matriz_sistema(n1[channel], n2[channel], n3[channel], n4[channel], n_i, n_r, R1, R2, R3, R4, R5, R6, d_pk, d_kz, d_sf, d_K, d_i, d_r)
    matriz_a = matriz_ideal(n2[channel], n2[channel], 1, R1_a, R2_a,10.2407, -10.2407, d_K-5, d_K,  d_i, d_r)

    matrices_RGB.append(matriz_RGB)
    matrices_a.append(matriz_a)
    Ma_a.append(matriz_a [1][1])
    Ma_RGB.append(matriz_RGB[1][1])
    
    width_outputs.append(int(width*(abs((-Ma_RGB[channel])/atenuacion))))
    height_outputs.append(int(height*(abs((-Ma_RGB[channel])/atenuacion))))

    width_outputs_a.append(int(width*(abs((-Ma_a[channel])/atenuacion))))
    height_outputs_a.append(int(height*(abs((-Ma_a[channel])/atenuacion))))

images = [Image.new("RGB", (width_outputs[_], height_outputs[_]), "white") for _ in range(3)]
pixels = [image.load() for image in images]

images_a = [Image.new("RGB", (width_outputs_a[_], height_outputs_a[_]), "white") for _ in range(3)]
pixels_a = [image8.load() for image8 in images_a]

for channel in range(3):
    pixels[channel] = ray_tracing_p(width, height, width_outputs[channel], height_outputs[channel], CHIEF_RAY, so, 1, RGB[channel], res, pixels[channel], matrices_RGB[channel], RGB_ref[channel], focales[channel],focales_k[channel],0)
    pixels[channel] = ray_tracing_p(width, height, width_outputs[channel], height_outputs[channel], PARALLEL_RAY, so, 1, RGB[channel], res, pixels[channel], matrices_RGB[channel], RGB_ref[channel],focales[channel],focales_k[channel],0)

    pixels_a[channel] = ray_tracing_p(width, height, width_outputs_a[channel], height_outputs_a[channel], CHIEF_RAY, so, 1, RGB_a[channel], res, pixels_a[channel], matrices_a[channel], RGB_ref[channel], focales_a[channel], focales_k_a[channel],1)
    pixels_a[channel] = ray_tracing_p(width, height, width_outputs_a[channel], height_outputs_a[channel], PARALLEL_RAY, so, 1, RGB_a[channel], res, pixels_a[channel], matrices_a[channel], RGB_ref[channel],focales_a[channel], focales_k_a[channel],1)

    if (interpolate):
        pixels[channel] = interpolation(pixels[channel], width_outputs[channel], height_outputs[channel], RGB_ref[channel])
        pixels_a[channel] = interpolation(pixels_a[channel], width_outputs_a[channel], height_outputs_a[channel], RGB_ref[channel])
        print("se hizo interpolacion para {}".format(RGB_ref[channel]))

    

imagen_final = image_sum(images[0], images[1], images[2])
imagen_final_a = image_sum(images_a[0], images_a[1], images_a[2])

#Validation----------------------------------------------------------------------------------------------------------------------------------------------------------------



#PLOTS----------------------------------------------------------------------------------------------------------------------------------------------------------------

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))


ax1.imshow(obj)
ax1.set_title('Cuerpo de estudio')
ax1.axis('off')

ax2.imshow(imagen_final)
ax2.set_title('Imagen corregida')
ax2.axis('off')

ax3.imshow(imagen_final_a)
ax3.set_title('Imagen con aberracion')
ax3.axis('off')
plt.show()

imagen_final_a.save('output.jpg', format='jpg')
