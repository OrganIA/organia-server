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

def getABO(ABOD, ABOR):
    if (ABOD == ABOR) or (ABOD == 'A' and ABOR == 'AB') or (ABOD == 'O' and ABOR == 'B'):
        return 1
    elif ABOD == 'O'and ABOR=='AB':
        return 0.1
    else:
        return 0

def getSC(tailleD, tailleR, poidsD, poidsR, ageR, sexD):

    fscD = 0.007184 * tailleD^0.725 * poidsD^0.725
    fscR = 0.007184 * tailleR^0.725 * poidsR^0.725

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

def getSurvPostGRF(riskPostGRF):
    return 0.6785748856^np.exp(riskPostGRF)

def getRiskPostGRF(fageR, fageD, fMAL, LnBili, LnDFG, sexRD):
    return (0.50608 * fageR + 0.50754 * fMAL + 0.40268 * LnBili - 0.54443 * LnDFG + 0.36262 * sexRD + 0.41714 * fageD)

def getFager(ageR):
    if ageR > 50:
        return 1
    else:
        return 0

def getfMAL(MAL, MAL2, MAL3):
    if MAL in ['Maladie valvulaire', 'Maladie congenitale', 'Maladie congenitale non Eisenmenger'] or MAL2 in ['Maladie valvulaire', 'Maladie congenitale', 'Maladie congenitale non Eisenmenger'] or MAL3 in ['Maladie valvulaire', 'Maladie congenitale', 'Maladie congenitale non Eisenmenger']:
        return 1
    else:
        return 0

def getLnBili(BILI, dateDBILI, dVarBio):
    if BILI == None or dateDBILI > dVarBio:
        return np.log(230)
    else:
        return np.log(min(230, max(5, BILI)))

def getLnDFG(DYAL, CREAT, dateDCREAT, dVarBio, DFG):
    if DYAL == 'O':
        np.log(15)
    elif CREAT == None or dateDCREAT > dVarBio:
        np.log(1)
    else:
        np.log(min(150, max(1, DFG)))

def getsexRD(sexD, sexR):
    if sexD == 'M' and sexR == 'F':
        return 1
    else:
        return 0

def getfageD(ageD):
    if ageD > 55:
        return 1
    else:
        return 0
# ********************Score CCP******************

def getScoreCCP(CCB, ABO, SC, survPostGRF):
    return CCB * difAge * ABO * SC * survPostGRF

# ***********************************************
ageR = 0
ageD = 0
MAL = 0
MAL2 = 0
MAL3 = 0
BILI = 0
dateDBILI = 0
dVarBio = 0
LnDFG = 0
sexD = 0
sexR = 0
DFG = 0
ABOD = 0
ABOR= 0
tailleD = 0
tailleR = 0
poidsD = 0
poidsR = 0

# *********
CCB = 0
TTLGP= 0 #durée du trajet entre les lieux de prélèvement et de greffe

ABO = getABO(ABOD, ABOR)
difAge = getDifAge(ageR, ageD)
fageD = getfageD(ageD)
sexRD = getsexRD(sexD, sexR)
LnBili = getLnBili(BILI, dateDBILI, dVarBio)
fMAL = getfMAL(MAL, MAL2, MAL3)
fageR = getFager(ageR)
riskPostGRF = getRiskPostGRF(ageR, ageD, MAL, LnBili, LnDFG, sexRD)
SC = getSC(tailleD, tailleR, poidsD, poidsR, ageR, sexD)
survPostGRF = getSurvPostGRF(riskPostGRF)
ScoreCCP = getScoreCCP(CCB, ABO, SC, survPostGRF)