from asyncio.windows_events import NULL
from math import ceil as round
from matplotlib.pyplot import get
from numpy import log as ln

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
F_Decile_PNi = None
F_Ln_DFG_LAi = None
F_Ln_BILI_LAi = None
ageR = None
urgence = None
XPC = None
PROBNP_Fct_Decile_PN_Dict = {
    1: 'Geeks', 2: 'For', 3: 'Geeks'}

def getF_ASCD(CEC2):
    if CEC2 == 'O':
        return 1
    else:
        return 0

#def getF_Decile_PNj(CEC2, CAT2, SIAV2, DBNB2):
#    if CEC2 == 'O'or CAT2 == 'O' or SIAV2 == 'B':
#        return 10
#    elif BNP2 == NULL and PROBNP2 == NULL:
#        return 1
#    elif PROBNP2 != NULL and Date_Courante - DPROBNB2 <= Delai_Var_Bio_LA:
#        res = 1 == 1 and 'test') or (2 == 2 and 'testtwo')
#    elif BNP2 != NULL and Date_Courante - DBNB2 <= Delai_Var_Bio_LA:
#
#    else:
#        return 1


#def getF_Ln_DFG_LAj():

#def getF_Ln_BILI_LAj():


def getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNj - 0.510058 * F_Ln_DFG_LAj + 0.615711 * F_Ln_BILI_LAj

def getICARj(F_RisquePreGRFj, C_ICAR):
    return max(0, round((F_RisquePreGRFj - C_ICAR) * 10))

def getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi):
    return 1.301335 * F_ASCD + 0.157691 * F_Decile_PNi - 0.510058 * F_Ln_DFG_LAi + 0.615711 * F_Ln_BILI_LAi

def getICARi(F_RisquePreGRFi, C_ICAR):
    return min(40, max(0, round((F_RisquePreGRFi - C_ICAR) * 10)))

def getICAR(CEC2, DRG2, ICARj, ICARi):
    if CEC2 != 'O' and DRG2 != 'O':
        return ICARj
    else:
        return max(ICARj, ICARi)

F_ASCD = getF_ASCD(CEC2)
F_RisquePreGRFj = getF_RisquePreGRFj(F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj)
F_RisquePreGRFi = getF_RisquePreGRFi(F_ASCD, F_Decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi)
C_ICAR = 1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)
ICARj = getICARj(F_RisquePreGRFj, C_ICAR)
ICARi = getICARi(F_RisquePreGRFi)
ICAR = getICAR(CEC2, DRG2, ICARj, ICARi)
F_ICAR = 1000 * ICAR / 40