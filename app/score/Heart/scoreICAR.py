from cmath import isnan
from math import ceil as round
from numpy import log as ln
import numpy as np

#------------------------------------Index de risque Cardiaque du jour (ICARj)------------------------------------------

#Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) du jour
def getF_Decile_PNj(CEC, CAT, SIAV, DBNP, BNP, PROBNP, Date_Courante, DPROBNB, Delai_Var_Bio_LA):
    if CEC == 'O'or CAT == 'O' or SIAV == 'B':
       return 10
    elif isnan(BNP) == True and isnan(PROBNP) == True:
       return 1
    elif isnan(PROBNP) != True and (Date_Courante - DPROBNB).days <= Delai_Var_Bio_LA:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1,2,3,4,5,6,7,8,9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
    elif isnan(BNP) != True and Date_Courante - DBNP <= Delai_Var_Bio_LA:
        conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
        res = [1,2,3,4,5,6,7,8,9]
        if BNP >= 2696:
            return 10
        for index, condition in enumerate(conditions):
            if BNP < condition:
                return res[index]
    else:
       return 1

#Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) du jour
def getF_DFGj(SEXR, AGER, CREAT):
    if SEXR == 'F':
        return 186.3 * (pow((CREAT/88.4),-1.154)) * (AGER*-0.203) * 0.742
    else:
        return 186.3 * (pow((CREAT/88.4),-1.154)) * (AGER*-0.203) * 1

def getF_Ln_DFG_LAj(DIA, CREAT, DCREAT, SEXR, AGER, Date_Courante, Delai_Var_Bio_LA):
    F_DFGj = getF_DFGj(SEXR, AGER, CREAT)
    x= np.timedelta64((Date_Courante - DCREAT), 'ns')
    day = x.astype('timedelta64[D]')
    DCDCRSub = day.astype(int)
    if DIA == 'O':
        return ln(15)
    elif isnan(CREAT) == True or DCDCRSub > Delai_Var_Bio_LA:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGj)))

#Fonction Bilirubine en Liste d’attente du jour
def getF_Ln_BILI_LAj(BILI, DBILI, Date_Courante, Delai_Var_Bio_LA):
    x= np.timedelta64((Date_Courante - DBILI), 'ns')
    day = x.astype('timedelta64[D]')
    DCDBLSub = day.astype(int)
    if isnan(BILI) == True or DCDBLSub > Delai_Var_Bio_LA:
        return ln(5)
    else:
        return ln(min(230, max(5, BILI)))

# La fonction de risque pré-greffe en liste d’attente du jour
def getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNj - 0.510058 * F_Ln_DFG_LAj + 0.615711 * F_Ln_BILI_LAj

#La function Index de risque Cardiaque du jour (ICARj)
def getICARj(F_RisquePreGRFj, C_ICAR):
    return max(0, round((F_RisquePreGRFj - C_ICAR) * 10))

#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------Index de risque avant perfusion ou implantation CEC (ICARi)------------------------

#Fonction Assistance de Courte Durée
def getF_ASCD(CEC):
        if CEC == 'O':
            return 1
        else:
            return 0

#Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) initiale
def getF_Decile_PNi(BNP_AVI, PBN_AVI,PROBNP, BNP, CEC, CAT, SIAV):
    if CEC == 'O' or CAT == 'O' or SIAV == 'B':
        return 10
    elif isnan(BNP_AVI) == True and isnan(PBN_AVI) == True:
        return 1
    elif isnan(PBN_AVI) != True:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1,2,3,4,5,6,7,8,9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
    elif isnan(BNP_AVI) != True:
        conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
        res = [1,2,3,4,5,6,7,8,9]
        if BNP >= 2696:
            return 10
        for index, condition in enumerate(conditions):
            if BNP < condition:
                return res[index]
    else:
        return 1

#Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) initiale
def getF_DFGi(SEXR, CRE_AVI, AGER):
    if SEXR == 'F':
        return 186.3 * ((CRE_AVI/88.4)*-1.154) * (AGER*(-0.203)) * 0.742
    else:
        return 186.3 * ((CRE_AVI/88.4)*-1.154) * (AGER*(-0.203)) * 1

def getF_Ln_DFG_LAi(DIA_AVI, CRE_AVI, SEXR, AGER):
    F_DFGi = getF_DFGi(SEXR, CRE_AVI, AGER)
    if DIA_AVI == 'O':
        return ln(15)
    elif isnan(CRE_AVI) == True:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGi)))

#Fonction Bilirubine en Liste d’attente initiale
def getF_Ln_BILI_LAi(BILI_AVI):
    if isnan(BILI_AVI) == True:
        return ln(5)
    else:
        return ln(min(230, max(5, BILI_AVI)))

#La fonction de risque pré-greffe en liste d’attente initiale
def getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNi - 0.510058 * F_Ln_DFG_LAi + 0.615711 * F_Ln_BILI_LAi

#Index de risque avant perfusion ou implantation CEC (ICARi)
def getICARi(F_RisquePreGRFi, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFi - C_ICAR) * 10)))

#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------Calcul de l’Index de Risque Cardiaque (ICAR)---------------------------------------

def getICAR(model):
    C_ICAR = 1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)
    F_Decile_PNj = getF_Decile_PNj(model.CEC, model.CAT, model.SIAV, model.DBNP, model.BNP, model.PROBNP, model.Date_Courante, model.DPROBNB, model.DelaiVarBioGRF)
    F_Ln_DFG_LAj = getF_Ln_DFG_LAj(model.DIA, model.CREAT, model.DCREAT, model.sexR, model.ageR, model.Date_Courante, model.DelaiVarBioGRF)
    F_Ln_BILI_LAj = getF_Ln_BILI_LAj(model.BILI, model.DBILI, model.Date_Courante, model.DelaiVarBioGRF)
    F_ASCD = getF_ASCD(model.CEC)
    F_RisquePreGRFj = getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj)
    ICARj = getICARj(F_RisquePreGRFj, C_ICAR)

    F_Ln_BILI_LAi = getF_Ln_BILI_LAi(model.BILI_AVI)
    F_Ln_DFG_LAi = getF_Ln_DFG_LAi(model.DIA_AVI, model.CRE_AVI, model.sexR, model.ageR)
    F_Decile_PNi = getF_Decile_PNi(model.BNP_AVI, model.PBN_AVI, model.PROBNP, model.BNP, model.CEC, model.CAT, model.SIAV)
    print(F_Decile_PNi)
    F_RisquePreGRFi = getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi)
    ICARi = getICARi(F_RisquePreGRFi, C_ICAR)

    if model.CEC != 'O' and model.DRG != 'O':
        return ICARj
    else:
        return max(ICARj, ICARi)

def checkICAR(ICAR):
    if ICAR > 40 or ICAR < 0:
        raise Exception ("Le score ICAR doit etre compris entre 0 et 40")
    else:
        return 0
#-----------------------------------------------------------------------------------------------------------------------