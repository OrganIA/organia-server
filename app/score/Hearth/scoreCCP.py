# Fonction d’appariement en âge entre donneur et receveur
def getDifAge(ageR, ageD):
    ageRD = ageR - ageD
    difAge = 0

    if ageRD < 0:
        difAge = (ageRD + 65) / 25
    else:
        difAge = 1 - (ageRD - 15) / 25
    if ageR >= 18:
        difAge = min(1, max(0, difAge))
    else:
        difAge = 1
    return (difAge)