from asyncio.windows_events import NULL
from math import ceil as round
from attr import NOTHING
from matplotlib.pyplot import get
from numpy import log as ln

#------------------------------------Index de risque Cardiaque du jour (ICARj)------------------------------------------

#Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) du jour
def getF_Decile_PNj(CEC2, CAT2, SIAV2, DBNB2, BNP2, PROBNP2, Date_Courante, DPROBNB2, Delai_Var_Bio_LA, PROBNP, BNP):
   if CEC2 == 'O'or CAT2 == 'O' or SIAV2 == 'B':
       return 10
   elif BNP2 == NULL and PROBNP2 == NULL:
       return 1
   elif PROBNP2 != NULL and Date_Courante - DPROBNB2 <= Delai_Var_Bio_LA:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1,2,3,4,5,6,7,8,9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
   elif BNP2 != NULL and Date_Courante - DBNB2 <= Delai_Var_Bio_LA:
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
def getF_DFGj(SEXR, AGER, CREAT2):
    if SEXR == 'F':
        return 186.3 * ((CREAT2/88.4)(-1.154)) * ((AGER)(-0.203)) * 0.742
    else:
        return 186.3 * ((CREAT2/88.4)(-1.154)) * ((AGER)(-0.203)) * 1

def getF_Ln_DFG_LAj(DIA2, CREAT2, DCREAT2, SEXR, AGER, Date_Courante, Delai_Var_Bio_LA):
    F_DFGj = getF_DFGj(CREAT2, AGER, SEXR)
    if DIA2 == 'O':
        return ln(15)
    elif CREAT2 == NULL or (Date_Courante - DCREAT2) > Delai_Var_Bio_LA:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGj)))

#Fonction Bilirubine en Liste d’attente du jour
def getF_Ln_BILI_LAj(BILI2, DBILI2, Date_Courante, Delai_Var_Bio_LA):
    if BILI2 == NULL or (Date_Courante - DBILI2) > Delai_Var_Bio_LA:
        return ln(5)
    else:
        ln(min(230, max(5, BILI2)))

#Fonction Assistance de Courte Durée
def getF_ASCD(CEC2):
    if CEC2 == 'O':
        return 1
    else:
        return 0

# La fonction de risque pré-greffe en liste d’attente du jour
def getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNj - 0.510058 * F_Ln_DFG_LAj + 0.615711 * F_Ln_BILI_LAj

#La function Index de risque Cardiaque du jour (ICARj)
def getICARj(F_RisquePreGRFj, C_ICAR):
    return max(0, round((F_RisquePreGRFj - C_ICAR) * 10))

#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------Index de risque avant perfusion ou implantation CEC (ICARi)------------------------

#Fonction Assistance de Courte Durée
def getF_ASCD(CEC2):
        if CEC2 == 'O':
            return 1
        else:
            return 0

#Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) initiale
def getF_Decile_PNi(BNP_AVI, PBN_AVI,PROBNP, BNP, CEC2, CAT2, SIAV2):
    if CEC2 == 'O' or CAT2 == 'O' or SIAV2 == 'B':
        return 10
    elif BNP_AVI == NULL and PBN_AVI == NULL:
        return 1
    elif PBN_AVI != NULL:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
        res = [1,2,3,4,5,6,7,8,9]
        if PROBNP >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP < condition:
                return res[index]
    elif BNP_AVI != NULL:
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
        return 186.3 * ((CRE_AVI/88.4)(-1.154)) * ((AGER)(-0.203)) * 0.742
    else:
        return 186.3 * ((CRE_AVI/88.4)(-1.154)) * ((AGER)(-0.203)) * 1

def getF_Ln_DFG_LAi(DIA_AVI, CRE_AVI, SEXR, AGER):
    F_DFGi = getF_DFGi(SEXR, CRE_AVI, AGER)
    if DIA_AVI == 'O':
        return ln(15)
    elif CRE_AVI == NULL:
        return ln(150)
    else:
        ln(min(150, max(1, F_DFGi)))

#Fonction Bilirubine en Liste d’attente initiale
def getF_Ln_BILI_LAi(BILI_AVI):
    if BILI_AVI == NULL:
        return ln(5)
    else:
        ln(min(230, max(5, BILI_AVI)))

#La fonction de risque pré-greffe en liste d’attente initiale
def getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNi - 0.510058 * F_Ln_DFG_LAi + 0.615711 * F_Ln_BILI_LAi

#Index de risque avant perfusion ou implantation CEC (ICARi)
def getICARi(F_RisquePreGRFi, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFi - C_ICAR) * 10)))

#-----------------------------------------------------------------------------------------------------------------------

#------------------------------------Calcul de l’Index de Risque Cardiaque (ICAR)---------------------------------------

#La function de calcul de l’Index de Risque Cardiaque (ICAR)
def getICAR(CEC2, DRG2, ICARj, ICARi):
    if CEC2 != 'O' and DRG2 != 'O':
        return ICARj
    else:
        return max(ICARj, ICARi)

#-----------------------------------------------------------------------------------------------------------------------


DRG2 =  None
CEC2 = None
CAT2 = None
SIAV2 = None
DBNB2 = None
DIA2 = None
CREAT2 = None
DCREAT2 = None
sexR = None
ageR = None
BILI2 = None
DBILI2 = None
BILI_AVI = None
DIA_AVI = None
CRE_AVI = None
BNP_AVI = None
PBN_AVI = None
PROBNP = None
BNP = None

C_ICAR = 1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)
F_Decile_PNj = getF_Decile_PNj(CEC2, CAT2, SIAV2, DBNB2)
F_Ln_DFG_LAj = getF_Ln_DFG_LAj(DIA2, CREAT2, DCREAT2, sexR, ageR)
F_Ln_BILI_LAj = getF_Ln_BILI_LAj(BILI2, DBILI2)
F_ASCD = getF_ASCD(CEC2)
F_RisquePreGRFj = getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj)
ICARj = getICARj(F_RisquePreGRFj, C_ICAR)

F_Ln_BILI_LAi = getF_Ln_BILI_LAi(BILI_AVI)
F_Ln_DFG_LAi = getF_Ln_DFG_LAi(DIA_AVI, CRE_AVI, sexR, ageR)
F_Decile_PNi = getF_Decile_PNi(BNP_AVI, PBN_AVI,PROBNP, BNP, CEC2, CAT2, SIAV2)
F_RisquePreGRFi = getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi)
ICARi = getICARi(F_RisquePreGRFi, C_ICAR)

ICAR = getICAR(CEC2, DRG2, ICARj, ICARi)
F_ICAR = 1000 * ICAR / 40