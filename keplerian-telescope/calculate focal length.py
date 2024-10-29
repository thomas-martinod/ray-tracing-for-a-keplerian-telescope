import numpy as np

# Lens data
refraction_NPK51_2 = {
        "R" : 1.5268,
        "G" : 1.5319,
        "B" : 1.5367,
        "Abbe" : 76.97,
        "R1": 12.61846363, 
        "R2": 35.89187673,
        "T": 42.81238979,
        "f": 21.86
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

# Lens maker's formula for each lens
def lens_maker_formula(R1, R2, n, T):
    if np.isinf(R2):  # For lenses with one flat surface
        return R1 / (n - 1)
    return 1 / ((n - 1) * (1 / R1 - 1 / R2 + ((n - 1) * T) / (n * R1 * R2)))

# Calculate focal lengths for each lens in green wavelength
f1 = lens_maker_formula(refraction_NPK51_2["R1"], refraction_NPK51_2["R2"], refraction_NPK51_2["G"], refraction_NPK51_2["T"])
f2 = lens_maker_formula(refraction_NKZFS4_2["R1"], refraction_NKZFS4_2["R2"], refraction_NKZFS4_2["G"], refraction_NKZFS4_2["T"])
f3 = lens_maker_formula(refraction_SF15_2["R1"], refraction_SF15_2["R2"], refraction_SF15_2["G"], refraction_SF15_2["T"])

# Calculate the combined focal length of the apochromat
combined_focal_length = 1 / (1 / f1 + 1 / f2 + 1 / f3)

print(f"Focal length for NPK51: {f1:.2f} mm")
print(f"Focal length for NKZFS4: {f2:.2f} mm")
print(f"Focal length for SF15: {f3:.2f} mm")
print(f"Combined focal length of the apochromat: {combined_focal_length:.2f} mm")
