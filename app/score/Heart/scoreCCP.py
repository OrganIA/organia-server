from datetime import datetime
import numpy as np


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


# Filtre ABO entre donneur et receveur
def getABO(ABOD, ABOR):
    if (ABOD == ABOR) or (ABOD == 'A' and ABOR == 'AB') or (ABOD == 'O' and ABOR == 'B'):
        return 1
    elif ABOD == 'O' and ABOR == 'AB':
        return 0.1
    else:
        return 0


# Appariement morphologique entre donneur et receveur
def getSC(tailleD, tailleR, poidsD, poidsR, ageR, sexD):
    fscD = 0.007184 * (pow(tailleD, 0.725)) * (pow(poidsD, 0.425))
    fscR = 0.007184 * (pow(tailleR, 0.725)) * (pow(poidsR, 0.425))

    if ageR >= 18:
        if 0.8 * fscR < fscD or (sexD == 'H' and poidsD >= 70):
            return 1
        else:
            return 0
    else:
        if (0.8 * fscR < fscD and 2 * fscR > fscD) or (sexD == 'H' and poidsD >= 70):
            return 1
        else:
            return 0


# Survie post-greffe à 1 an
def getSurvPostGRF(riskPostGRF):
    return pow(0.6785748856, np.exp(riskPostGRF))


# Fonction du tri des patients par age ou chances de survie
def triSurvPostGRF(survPostGRF, ageR):
    if survPostGRF > 0.5 or ageR < 18:
        return 1
    else:
        return 0


# Fonction de risque post-greffe
def getRiskPostGRF(fageR, fageD, fMAL, LnBili, LnDFG, sexRD):
    return (0.50608 * fageR + 0.50754 * fMAL + 0.40268 * LnBili - 0.54443 * LnDFG + 0.36262 * sexRD + 0.41714 * fageD)


# Fonction sur l’âge du receveur
def getFager(ageR):
    if ageR > 50:
        return 1
    else:
        return 0


# Fonction sur la maladie initiale du receveur
def getfMAL(MAL, MAL2, MAL3):
    mal = ['Maladie valvulaire', 'Maladie congenitale', 'Maladie congenitale non Eisenmenger']
    if MAL in mal or MAL2 in mal or MAL3 in mal:
        return 1
    else:
        return 0


# Fonction bilirubine pour le post-greffe
def getLnBili(BILI, dateDBILI, dVarBio):
    x = np.timedelta64((datetime.now() - dateDBILI), 'ns')
    day = x.astype('timedelta64[D]')
    dateDBILI = day.astype(int)

    if np.isnan(BILI) == True or dateDBILI > dVarBio:
        return np.log(230)
    else:
        return np.log(min(230, max(5, BILI)))


# Fonction du Débit de Filtration Glomérulaire pour le post-greffe
def getLnDFG(DIA, CREAT, DCREAT, dVarBio, DFG):
    x = np.timedelta64((datetime.now() - DCREAT), 'ns')
    day = x.astype('timedelta64[D]')
    DCREAT = day.astype(int)

    if DIA == 'O':
        return np.log(15)
    elif np.isnan(CREAT) == True or DCREAT > dVarBio:
        return np.log(1)
    else:
        return np.log(min(150, max(1, DFG)))


# Fonction sur l’appariement du sexe entre donneur et receveur
def getsexRD(sexD, sexR):
    if sexD == 'M' and sexR == 'F':
        return 1
    else:
        return 0


# Fonction sur l’âge du donneur
def getfageD(ageD):
    if ageD > 55:
        return 1
    else:
        return 0


# Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) du jour
def getF_DFGj(SEXR, AGER, CREAT):
    if SEXR == 'F':
        return 186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(AGER, -0.203)) * 0.742
    else:
        return 186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(AGER, -0.203)) * 1


# ********************Score CCP******************

def getScoreCCP(model, CCB):
    F_DFGj = getF_DFGj(model.sexR, model.ageR, model.CREAT)
    LnDFG = getLnDFG(model.DIA, model.CREAT, model.DCREAT, model.DelaiVarBioGRF, F_DFGj)
    fageD = getfageD(model.ageD)
    sexRD = getsexRD(model.sexD, model.sexR)
    LnBili = getLnBili(model.BILI, model.dateDBILI, model.DelaiVarBioGRF)
    fMAL = getfMAL(model.MAL, model.MAL2, model.MAL3)
    fageR = getFager(model.ageR)
    riskPostGRF = getRiskPostGRF(fageR, fageD, fMAL, LnBili, LnDFG, sexRD)
    difAge = getDifAge(model.ageR, model.ageD)
    ABO = getABO(model.ABOD, model.ABOR)
    SC = getSC(model.tailleD, model.tailleR, model.poidsD, model.poidsR, model.ageR, model.sexD)
    survPostGRF = getSurvPostGRF(riskPostGRF)
    trisurvpostgrf = triSurvPostGRF(survPostGRF, model.ageR)
    return CCB * difAge * ABO * SC  * trisurvpostgrf

# ***********************************************