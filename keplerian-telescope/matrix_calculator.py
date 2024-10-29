# import libraries
import numpy as np
from data import get_data


def traslation_matrix(d : float, n : float) -> np.array:
    return np.array([[1, d/n], [0, 1]])


def refraction_matrix(n1 : float, n2 : float, R : float) -> np.array:
    # Imagina que vas de izquierda a derecha, R es positivo siendo visto concava
    # n1 antes de la refracción y n2 después
    return np.array([[1, 0],[(n1-n2)/R, 1]])


def reflection_matrix(n : float, R : float) -> np.array:
    return np.array([[1, 0],[2*n/R, 1]])


def thick_lens(n_in, n_out, R1, R2, thickness):
    # n_in: Adentro de la lente
    # n_out: Afuera de la lente
    # R1: Positivo concava de izquierda a derecha (convergente)
    # R2: Positivo concava de derecha a izquierda (divergente)
    return (refraction_matrix(n1=n_in, n2=n_out, R=R2) @ traslation_matrix(thickness, n_in) @ refraction_matrix(n1=n_out, n2=n_in, R = R1))


def thin_lens(f):
    return np.array([[1, 0], [-1/f, 1]])


def simple_system(n_in: float, n_out: float, objective: dict, eyepiece: dict) -> np.array:
    # Without the eye and without aberrations
    O = thick_lens(n_in, n_out, objective["R"], -objective["R"], objective["T"])
    T = traslation_matrix(objective["f"] + eyepiece["f"], n_out)
    E = thick_lens(n_in, n_out, eyepiece["R"], -eyepiece["R"], eyepiece["T"])

    return (E @ T) @ O


