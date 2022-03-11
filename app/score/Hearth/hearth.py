from asyncio.windows_events import NULL
from math import ceil as round
from attr import NOTHING
from matplotlib.pyplot import get
from numpy import log as ln

BILI2 = None
DBILI2 = None
DBNB2 = None
CEC2 = None
DRG2 = None
CAT2 = None
SIAV2 = None
BNP2 = None
PROBNP2 = None
Date_Courante = None
Delai_Var_Bio_LA = None
DPROBNB2 = None
F_Decile_PNj = None
F_Ln_DFG_LAj = None
F_Ln_BILI_LAj = None
DIA2 = None
CREAT2 = None
DCREAT2 = None
F_Decile_PNi = None
F_Ln_DFG_LAi = None
F_Ln_BILI_LAi = None
ageR = None
sexR = None
urgence = None
XPC = None

#------------------------------------Index de risque Cardiaque du jour (ICARj)------------------------------------------

#Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) du jour
def getF_Decile_PNj(CEC2, CAT2, SIAV2, DBNB2):
   if CEC2 == 'O'or CAT2 == 'O' or SIAV2 == 'B':
       return 10
   elif BNP2 == NULL and PROBNP2 == NULL:
       return 1
   elif PROBNP2 != NULL and Date_Courante - DPROBNB2 <= Delai_Var_Bio_LA:
        conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000]
        res = [1,2,3,4,5,6,7,8,9]
        if PROBNP2 >= 11332:
            return 10
        for index, condition in enumerate(conditions):
            if PROBNP2 < condition:
                return res[index]
   elif BNP2 != NULL and Date_Courante - DBNB2 <= Delai_Var_Bio_LA:
        conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
        res = [1,2,3,4,5,6,7,8,9]
        if BNP2 >= 2696:
            return 10
        for index, condition in enumerate(conditions):
            if BNP2 < condition:
                return res[index]
   else:
       return 1

#Fonction Débit de Filtration Glomérulaire en Liste d’attente (méthode MDRD) du jour
def getF_DFGj(SEXR, AGER, CREAT2):
    if SEXR == 'F':
        return 186.3 * ((CREAT2/88.4)(-1.154)) * ((AGER)(-0.203)) * 0.742
    else:
        return 186.3 * ((CREAT2/88.4)(-1.154)) * ((AGER)(-0.203)) * 1

def getF_Ln_DFG_LAj(DIA2, CREAT2, DCREAT2, SEXR, AGER):
    F_DFGj = getF_DFGj(CREAT2, AGER, SEXR)
    if DIA2 == 'O':
        return ln(15)
    elif CREAT2 == NULL or (Date_Courante - DCREAT2) > Delai_Var_Bio_LA:
        return ln(150)
    else:
        return ln(min(150, max(1, F_DFGj)))

#Fonction Bilirubine en Liste d’attente du jour
def getF_Ln_BILI_LAj(BILI2, DBILI2):
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

def getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNi - 0.510058 * F_Ln_DFG_LAi + 0.615711 * F_Ln_BILI_LAi

def getICARi(F_RisquePreGRFi, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFi - C_ICAR) * 10)))

#-----------------------------------------------------------------------------------------------------------------------

#La function de calcul de l’Index de Risque Cardiaque (ICAR)
def getICAR(CEC2, DRG2, ICARj, ICARi):
    if CEC2 != 'O' and DRG2 != 'O':
        return ICARj
    else:
        return max(ICARj, ICARi)

C_ICAR = 1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)

Decile_PNj = getF_Decile_PNj(CEC2, CAT2, SIAV2, DBNB2)
F_Ln_DFG_LAj = getF_Ln_DFG_LAj(DIA2, CREAT2, DCREAT2, sexR, ageR)
F_Ln_BILI_LAj = getF_Ln_BILI_LAj(BILI2, DBILI2)
F_ASCD = getF_ASCD(CEC2)
F_RisquePreGRFj = getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj)
ICARj = getICARj(F_RisquePreGRFj, C_ICAR)

F_RisquePreGRFi = getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi)
ICARi = getICARi(F_RisquePreGRFi)

ICAR = getICAR(CEC2, DRG2, ICARj, ICARi)
F_ICAR = 1000 * ICAR / 40