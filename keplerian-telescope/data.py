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
    return objective_lens, eyepiece_lens, rgb, refraction_NBK7


def get_aberration_data():

    refraction_NPK51_1 = {
        "R" : 1.5268,
        "G" : 1.5319,
        "B" : 1.5367,
        "Abbe" : 76.97,
        "R1": 187.74016, 
        "R2": 221.53356,
        "T": 4.07773,
        "f": 268.14
    }
    refraction_NKZFS4_1 = {
        "R" : 1.6098,
        "G" : 1.6202,
        "B" : 1.6300,
        "Abbe" : 44.49,
        "R1": 221.53356, 
        "R2": 303.86069,
        "T": 51.70174
    }
    refraction_SF15_1 = {
        "R" : 1.6932,
        "G" : 1.7105,
        "B" : 1.7280,
        "Abbe" : 30.07,
        "R1": 303.86069, 
        "R2": np.inf,
        "T": 5
    }

    refraction_NPK51_2 = {
        "R" : 1.5268,
        "G" : 1.5319,
        "B" : 1.5367,
        "Abbe" : 76.97,
        "R1": 12.61846363, 
        "R2": 35.89187673,
        "T": 42.81238979,
        "f": 15.43
    }
    refraction_NKZFS4_2 = {
        "R" : 1.6098,
        "G" : 1.6202,
        "B" : 1.6300,
        "Abbe" : 44.49,
        "R1": 35.89187673, 
        "R2": 49.78133573,
        "T": 6.835217
    }
    refraction_SF15_2 = {
        "R" : 1.6932,
        "G" : 1.7105,
        "B" : 1.7280,
        "Abbe" : 30.07,
        "R1": 49.78133573, 
        "R2": np.inf,
        "T": 5
    }

    return refraction_NPK51_1, refraction_NKZFS4_1,refraction_SF15_1, refraction_NPK51_2, refraction_NKZFS4_2, refraction_SF15_2

    

