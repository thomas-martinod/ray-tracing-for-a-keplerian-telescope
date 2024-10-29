# -*- coding: utf-8 -*-
"""
Title: symple optical lens simulation

Description: Python script that performs the optical lens simulation by two options {thin lens and magnification}

Created on March 12, 2023

@author: Raul Castaneda, universidad EAFIT
version 1.0
"""

# import libraries
import sympy as sp


# function to simulate a thin lens
def thin_lens(objDist, imgDist, fDist):
    # objDist = object distance
    # imgDist = image distance
    # fDist = focal distance
    if objDist == 0:
        objDist = sp.Symbol('objDist')
        lensEquation = ((1 / objDist) + (1 / imgDist)) - (1 / fDist)
        solution = sp.solve(lensEquation)
        print("the object distance is :", solution, "mm")

    elif imgDist == 0:
        imgDist = sp.Symbol('imgDist')
        lensEquation = ((1 / objDist) + (1 / imgDist)) - (1 / fDist)
        solution = sp.solve(lensEquation)
        print("the image distance is :", solution, "mm")

    elif fDist == 0:
        fDist = sp.Symbol('fDist')
        lensEquation = ((1 / objDist) + (1 / imgDist)) - (1 / fDist)
        solution = sp.solve(lensEquation)
        print("the focal distance is :", solution, "mm")

    return solution


# function to simulate a magnification
def magn_transversal(objDist, imgDist, magn):
    # objDist = object distance
    # imgDist = image distance
    # M = magnification
    if objDist == 0:
        objDist = sp.Symbol('objDist')
        magnEquation = ((imgDist / objDist) - magn)
        solution = sp.solve(magnEquation)
        print("the object distance is :", solution, "mm")

    elif imgDist == 0:
        imgDist = sp.Symbol('imgDist')
        magnEquation = ((imgDist / objDist) - magn)
        solution = sp.solve(magnEquation)
        print("the image distance is :", solution, "mm")

    elif magn == 0:
        magn = sp.Symbol('fDist')
        magnEquation = ((imgDist / objDist) - magn)
        solution = sp.solve(magnEquation)
        print("the focal distance is :", solution, "mm")

    return solution


# calling magn_transversal

print("Please, input the optical parameters [object distance, image distance and magnification]")
print("If you don't know some parameter, input 0)")
objDist = float(input("Please, input the object distance in mm "))
imgDist = float(input("Please, input the image distance in mm "))
magn = float(input("Please, input the magnification system "))

solution = magn_transversal(objDist, imgDist, magn)


# calling thin_lens
'''
print("Please, input the optical parameters [object distance, image distance and focal distace]")
print("If you don't know some parameter, input 0)")
objDist = float(input("Please, input the object distance in mm "))
imgDist = float(input("Please, input the image distance in mm "))
fDist = float(input("Please, input the focal distance in mm "))

solution = thin_lens(objDist, imgDist, fDist)
'''
