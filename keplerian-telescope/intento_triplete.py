def get_data_triplete():
    # https://erepo.uef.fi/bitstream/handle/123456789/22245/urn_nbn_fi_uef-20200556.pdf

    rgb = {
        "R" : 645e-6,
        "G" : 510e-6,
        "B" : 440e-6
    }

    # https://refractiveindex.info/?shelf=glass&book=SCHOTT-PK&page=N-PK51
    refraction_NPK51 = {
        "R" : 1.5268,
        "G" : 1.5319,
        "B" : 1.5367,
        "Abbe" : 76.97
    }

    # https://refractiveindex.info/?shelf=glass&book=SCHOTT-KzFS&page=N-KZFS4
    refraction_NKZFS4 = {
        "R" : 1.6098,
        "G" : 1.6202,
        "B" : 1.6300,
        "Abbe" : 44.49
    }

    # https://refractiveindex.info/?shelf=glass&book=SCHOTT-SF&page=SF15
    refraction_SF15 = {
        "R" : 1.6932,
        "G" : 1.7105,
        "B" : 1.7280,
        "Abbe" : 30.07
    }
    return refraction_NPK51, refraction_NKZFS4, refraction_SF15



