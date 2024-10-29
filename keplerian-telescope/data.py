def get_data():
    objective_lens = {
        "R": 772, # mm
        "T": 3, # mm
        "D": 50.8, #mm
        "f": 750 #mm
        }

    eyepiece_lens = {
        "R": 19.9, # mm
        "T": 3.9, # mm
        "D": 12.7, #mm
        "f": 20 #mm
        }

    rgb = {
        "R" : 645e-6,
        "G" : 510e-6,
        "B" : 440e-6
    }

    refraction_crown = {
        "R" : 1.509137,
        "G" : 1.515446,
        "B" : 1.52094
    }
    

    # refraction_crown = {
    #     "R" : 0.0000001,
    #     "G" : 1.515446,
    #     "B" : 100.52094
    # }
    return objective_lens, eyepiece_lens, rgb, refraction_crown