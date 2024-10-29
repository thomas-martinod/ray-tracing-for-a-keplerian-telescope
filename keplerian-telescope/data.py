import numpy as np
def get_data():
    objective_lens = {
        "R": 205.0,  # Reduced radius of curvature
        "T": 6.2,  # Thickness
        "D": 50.8,  # Diameter
        "f": 200  # Reduced focal length to 200 mm
    }

    eyepiece_lens = {
        "R": 25.2,  # Slightly increased radius of curvature
        "T": 3.4,  # Thickness
        "D": 12.7,  # Diameter
        "f": 25.0 # focal length for lower magnification
    }

    rgb = {
        "R" : 645e-6,
        "G" : 510e-6,
        "B" : 440e-6
    }

    refraction_NBK7 = {
        "R" : 1.5147,
        "G" : 1.5208,
        "B" : 1.5263
    }

    apocromat = {
        "R1": 200,
        "R2": 200,
        "R3": 200,
        "R4": np.inf,
        ""


    }

    return objective_lens, eyepiece_lens, rgb, refraction_NBK7, apocromat
