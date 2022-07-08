import numpy as np
from datetime import datetime
from test import sample1
from cmath import isnan
from math import ceil as round
from numpy import log as ln


class Model:
    def __init__(self, data):
        self.ageR = (data['D_INSC'] - data['R_D_NAI']).days / 365
        self.ageD = (data['D_INSC'] - data['R_D_NAI']).days / 365
        self.sexD = data['SEXD']
        self.sexR = data['SEXR']
        self.tailleD = data['TAILLED']
        self.tailleR = data['TAILLER']
        self.poidsD = data['POIDSD']
        self.poidsR = data['POIDSR']

        self.DRG = data['DRG']
        self.CEC = data['CEC']
        self.DCEC = data['DCEC']
        self.CAT = data['CAT']
        self.SIAV = data['SIAV']
        self.DIA = data['DIA']
        self.CREAT = data['CREAT']
        self.DCREAT = data['DCREAT']
        self.DBILI = data['DBILI']
        self.BILI_AVI = data['BILI_AVI']
        self.DIA_AVI = data['DIA_AVI']
        self.CRE_AVI = data['CRE_AVI']
        self.BNP_AVI = data['BNP_AVI']
        self.PBN_AVI = data['PBN_AVI']
        self.PROBNP = data['PROBNP']
        #self.Date_Courante = datetime.now()
        self.Date_Courante = data['D_PREL']
        self.DelaiVarBioGRF = getDelaiVarBioGRF(self.CEC, self.DRG)
        self.DPROBNB = data['DPROBNP']
        self.BNP = data['BNP']

        self.urgence = data['URGENCE']
        self.XPC = data['XPC']
        self.KXPC = data['KXPC']
        self.DAURG = (data['D_PREL'] - data['D_URGENCE']).days / 30.5
        self.DA = (data['D_PREL'] - data['D_INSC']).days / 30.5

        self.MAL = data['MAL']
        self.MAL2 = data['MAL2']
        self.MAL3 = data['MAL3']
        self.BILI = data['BILI']
        self.dateDBILI = data['DBILI']
        self.ABOD = data['ABOD']
        self.ABOR = data['ABOR']
        self.TTLGP = data['TTLGP']
        self.DBNP = data['DBNP']

def getDelaiVarBioGRF(CEC, DRG):
    if CEC != 'O' and DRG != 'O':
        return 105
    else:
        return 4


# ************************Score NACG*************************

def getScoreNACG(scoreCCP, TTLGP):
    MG = 1 / np.exp(0.0000002 * pow(TTLGP, 2.9))
    return scoreCCP * MG


# ***********************************************************
model = Model(sample1)

scoreICAR = checkICAR(getICAR(model))
F_ICAR = 1000 * scoreICAR / 40
scoreCCB = getScoreCCB(model, F_ICAR)
scoreCCP = getScoreCCP(model, scoreCCB)
NAGC = getScoreNACG(scoreCCP, model.TTLGP)

# Composant Adulte Standard -> CAS
def getCAS(ageR, urgence, fICAR):
    if ageR >= 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
        if fICAR < 775:
            return fICAR
        else:
            return fICAR + 51
    else:
        return 0


# verification de la CAS
def checkCAS(CAS):
    if CAS < 0 or (CAS > 775 and CAS < 826) or CAS > 1051:
        raise Exception("La composante adulte standard doit se situer entre 0 et 775 points ou 826 et 1051 points")
    else:
        return 0


# Composante Expert Adulte -> XPCA
def getXPCA(ageR, urgence, XPC, fICAR, KXPC, DAURG):
    if ageR >= 18 and urgence == 'XPCA':
        if XPC == 0:
            return max(fICAR, KXPC)
        else:
            return max(fICAR, KXPC * max(0, min(1, DAURG / XPC)))
    else:
        return 0


# Verification de la XPCA
def checkXPCA(XPCA):
    if XPCA != 900:
        raise Exception("La composante XPCA ne peut etre differente de 900 points")
    else:
        return 0


# Composante Pédiatrique Standard -> CPS
def getCPS(ageR, urgence, DA):
    if ageR < 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
        return (775 + 50 * max(0, min(1, DA / 24)))
    else:
        return 0


def checkCPS(CPS):
    if CPS < 776 or CPS > 825:
        raise Exception("La composante pediatrique standard doit se situer entre 776 et 825 points")
    else:
        return 0


# Composante Expert Pédiatrique -> XPCP
def getXPCP(urgence, KXPC, DAURG):
    if urgence == 'XPCP1' or urgence == 'XPCP2':
        return (KXPC + 50 * max(0, min(1, DAURG / 24)))
    else:
        return 0


def checkXPCP(urgence, XPCP):
    if urgence == 'XPCP1' and XPCP < 1102 or XPCP > 1151:
        raise Exception("Le score XPCP pour une urgence de niveau 1 doit se situer entre 1102 et 1151 points")
    elif urgence == 'XPCP2' and XPCP < 1051 or XPCP > 1101:
        raise Exception("Le score XPCP pour une urgence de niveau 2 doit se situer entre 1051 et 1101 points")
    else:
        return 0


def getScoreCCB(model, F_ICAR):
    CAS = getCAS(model.ageR, model.urgence, F_ICAR)
    XPCA = getXPCA(model.ageR, model.urgence, model.XPC, F_ICAR, model.KXPC, model.DAURG)
    CPS = getCPS(model.ageR, model.urgence, model.DA)
    XPCP = getXPCP(model.urgence, model.KXPC, model.DAURG)
    return (CAS + XPCA + CPS + XPCP)


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
def getLnBili(BILI, dateDBILI, dVarBio, date_courante):
    x = np.timedelta64((date_courante - dateDBILI), 'ns')
    day = x.astype('timedelta64[D]')
    dateDBILI = day.astype(int)

    if np.isnan(BILI) == True or dateDBILI > dVarBio:
        return np.log(230)
    else:
        return np.log(min(230, max(5, BILI)))


# Fonction du Débit de Filtration Glomérulaire pour le post-greffe
def getLnDFG(DIA, CREAT, DCREAT, dVarBio, DFG, date_courante):
    x = np.timedelta64((date_courante - DCREAT), 'ns')
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
    LnDFG = getLnDFG(model.DIA, model.CREAT, model.DCREAT, model.DelaiVarBioGRF, F_DFGj, model.Date_Courante)
    fageD = getfageD(model.ageD)
    sexRD = getsexRD(model.sexD, model.sexR)
    LnBili = getLnBili(model.BILI, model.dateDBILI, model.DelaiVarBioGRF, model.Date_Courante)
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



# ------------------------------------Index de risque Cardiaque du jour (ICARj)------------------------------------------

# Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) du jour
def getF_Decile_PNj(CEC, CAT, SIAV, DBNP, BNP, PROBNP, Date_Courante, DPROBNB, Delai_Var_Bio_LA):
    if CEC == 'O' or CAT == 'O' or SIAV == 'B':
        return 10
    elif isnan(BNP) is True and isnan(PROBNP) is True:
        return 1
    elif isnan(PROBNP) is not True and (Date_Courante - DPROBNB).days <= Delai_Var_Bio_LA:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
    elif isnan(BNP) is not True and (Date_Courante - DBNP).days <= Delai_Var_Bio_LA:
        conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
        res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if BNP >= 2696:
            return 10
        for index, condition in enumerate(conditions):
            if BNP < condition:
                return res[index]
    else:
        return 1


# Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) du jour
def getF_DFGj(SEXR, AGER, CREAT):
    if SEXR == 'F':
        return 186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(AGER, -0.203)) * 0.742
    else:
        return 186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(AGER, -0.203)) * 1


def getF_Ln_DFG_LAj(DIA, CREAT, DCREAT, SEXR, AGER, Date_Courante, Delai_Var_Bio_LA):
    F_DFGj = getF_DFGj(SEXR, AGER, CREAT)
    if DIA == 'O':
        return ln(15)
    elif isnan(CREAT) is True or (Date_Courante - DCREAT).days > Delai_Var_Bio_LA:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGj)))


# Fonction Bilirubine en Liste d’attente du jour
def getF_Ln_BILI_LAj(BILI, DBILI, Date_Courante, Delai_Var_Bio_LA):
    if isnan(BILI) is True or (Date_Courante - DBILI).days > Delai_Var_Bio_LA:
        return ln(5)
    else:
        return ln(min(230, max(5, BILI)))


# Fonction Assistance de Courte Durée
def getF_ASCD(CEC):
    if CEC == 'O':
        return 1
    else:
        return 0


# La fonction de risque pré-greffe en liste d’attente du jour
def getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNj - 0.510058 * F_Ln_DFG_LAj + 0.615711 * F_Ln_BILI_LAj


# La function Index de risque Cardiaque du jour (ICARj)
def getICARj(F_RisquePreGRFj, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFj - C_ICAR) * 10)))


# -----------------------------------------------------------------------------------------------------------------------

# ------------------------------------Index de risque avant perfusion ou implantation CEC (ICARi)------------------------

# Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) initiale
def getF_Decile_PNi(BNP_AVI, PBN_AVI, PROBNP, BNP, CEC, CAT, SIAV):
    if CEC == 'O' or CAT == 'O' or SIAV == 'B':
        return 10
    elif isnan(BNP_AVI) is True and isnan(PBN_AVI) is True:
        return 1
    elif isnan(PBN_AVI) is not True:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
    elif isnan(BNP_AVI) is not True:
        conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
        res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        if BNP >= 2696:
            return 10
        for index, condition in enumerate(conditions):
            if BNP < condition:
                return res[index]
    else:
        return 1


# Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) initiale
def getF_DFGi(SEXR, CRE_AVI, AGER):
    if SEXR == 'F':
        return 186.3 * ((CRE_AVI / 88.4) * -1.154) * (pow(AGER, -0.203)) * 0.742
    else:
        return 186.3 * ((CRE_AVI / 88.4) * -1.154) * (pow(AGER, -0.203)) * 1


def getF_Ln_DFG_LAi(DIA_AVI, CRE_AVI, SEXR, AGER):
    F_DFGi = getF_DFGi(SEXR, CRE_AVI, AGER)
    if DIA_AVI == 'O':
        return ln(15)
    elif isnan(CRE_AVI) is True:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGi)))


# Fonction Bilirubine en Liste d’attente initiale
def getF_Ln_BILI_LAi(BILI_AVI):
    if isnan(BILI_AVI) is True:
        return ln(5)
    else:
        return ln(min(230, max(5, BILI_AVI)))


# La fonction de risque pré-greffe en liste d’attente initiale
def getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNi - 0.510058 * F_Ln_DFG_LAi + 0.615711 * F_Ln_BILI_LAi


# Index de risque avant perfusion ou implantation CEC (ICARi)
def getICARi(F_RisquePreGRFi, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFi - C_ICAR) * 10)))


# -----------------------------------------------------------------------------------------------------------------------

# ------------------------------------Calcul de l’Index de Risque Cardiaque (ICAR)---------------------------------------

def getICAR(model):
    C_ICAR = 1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)
    F_Decile_PNj = getF_Decile_PNj(model.CEC, model.CAT, model.SIAV, model.DBNP, model.BNP, model.PROBNP,
                                   model.Date_Courante, model.DPROBNB, model.DelaiVarBioGRF)
    F_Ln_DFG_LAj = getF_Ln_DFG_LAj(model.DIA, model.CREAT, model.DCREAT, model.sexR, model.ageR, model.Date_Courante,
                                   model.DelaiVarBioGRF)
    F_Ln_BILI_LAj = getF_Ln_BILI_LAj(model.BILI, model.DBILI, model.Date_Courante, model.DelaiVarBioGRF)
    F_ASCD = getF_ASCD(model.CEC)
    F_RisquePreGRFj = getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj)
    ICARj = getICARj(F_RisquePreGRFj, C_ICAR)

    F_Ln_BILI_LAi = getF_Ln_BILI_LAi(model.BILI_AVI)
    F_Ln_DFG_LAi = getF_Ln_DFG_LAi(model.DIA_AVI, model.CRE_AVI, model.sexR, model.ageR)
    F_Decile_PNi = getF_Decile_PNi(model.BNP_AVI, model.PBN_AVI, model.PROBNP, model.BNP, model.CEC, model.CAT,
                                   model.SIAV)
    F_RisquePreGRFi = getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi)
    ICARi = getICARi(F_RisquePreGRFi, C_ICAR)

    if model.CEC != 'O' and model.DRG != 'O':
        return ICARj
    else:
        return max(ICARj, ICARi)


def checkICAR(ICAR):
    if ICAR > 40 or ICAR < 0:
        raise Exception("Le score ICAR doit etre compris entre 0 et 40")
    else:
        return ICAR
# -----------------------------------------------------------------------------------------------------------------------