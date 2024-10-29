import utilities as ut
from data import get_data, get_aberration_data
import numpy as np
from PIL import Image

def interpolate(r, g, b):
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

        return r_image, g_image, b_image


def main():
    print("Which celestial object would you like to view?")
    print("Options: Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus")
    
    choice = input("Enter the name of the object: ").strip().capitalize()

    image_directory = "keplerian-telescope/figs/"
    celestial_objects = {
        "Mercury": "Mercury.jpg",
        "Venus": "Venus.jpg",
        "Earth": "Earth.jpg",
        "Mars": "Mars.jpg",
        "Jupiter": "Jupiter.jpg",
        "Saturn": "Saturn.jpg",
        "Uranus": "Uranus.jpg"
    }

    aberration = input("Correct Aberration? (y/n): ").strip().capitalize()

    options = ["Y", "N"]

    if aberration in options:
        if choice in celestial_objects:
            image_path = image_directory + celestial_objects[choice]
            print(f"Loading image for {choice} from {image_path}")

            object = ut.imageRead(image_path)

            red, green, blue = object.split()

            if aberration == "N":

                objective_lens, eyepiece_lens, _, _ = get_data()

                magni = -objective_lens["f"]/eyepiece_lens["f"]

                width, height = object.size

                width_output = int(width*(abs(magni)))
                height_output = int(height*(abs(magni)))

                b = ut.keplerian_ray_tracing(blue, width_output, height_output, "B", n_air=1.0003)
                r = ut.keplerian_ray_tracing(red, width_output, height_output, "R",  n_air=1.0003)
                g = ut.keplerian_ray_tracing(green, width_output, height_output, "G", n_air=1.0003)

                r_image, g_image, b_image = interpolate(r, g, b)
            
                # Fusiona los canales de nuevo en una imagen RGB
                Output_image = Image.merge("RGB", (r_image, g_image, b_image))

                # Muestra la imagen procesada
                ut.imageShow([object, Output_image], [f"Original {choice} Image", f'Processed {choice} Image'])

                ut.imageSave(Output_image, choice)    
            elif aberration == "Y":
                refraction_NPK51_1, _, _, refraction_NPK51_2, _, _= get_aberration_data()
                magni = -refraction_NPK51_1["f"]/refraction_NPK51_2["f"]

                width, height = object.size

                width_output = int(width*(abs(magni)))
                height_output = int(height*(abs(magni)))
                
                print("Correcting Aberrations")
                b_a = ut.correct_aberration(blue, width_output + 10, height_output + 10, "B", n_air=1.0003)
                r_a = ut.correct_aberration(red, width_output + 10, height_output +10, "R",  n_air=1.0003)
                g_a = ut.correct_aberration(green, width_output +10, height_output + 10, "G", n_air=1.0003)

                r_a, g_a, b_a = interpolate(r_a, g_a, b_a)

                corrected = Image.merge("RGB", (r_a, g_a, b_a))

                ut.imageShow([object, corrected], [f"Original {choice} Image", f'Corrected {choice} Image'])
                ut.imageSave(corrected, choice, corrected = True)  

        else:
            print("Invalid choice. Please restart the program and select a valid celestial object.")
            return

    else:
        print("Invalid choice. Please restart the program and select a valis aberration option.")
        return

main()