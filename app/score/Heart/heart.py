from score.Heart.scoreICAR import getICAR
from score.Heart.scoreCCP import getScoreCCP
from score.Heart.scoreCCB import getScoreCCB

# ************************Score NACG*************************


def getScoreNACG(scoreCCP, TTLGP):
    MG = 1 / np.exp(0.00000002 * TTLGP^2.9)
    return scoreCCP * MG

# ***********************************************************



ageR = None
ageD = None
sexD = None
sexR = None

#--------------------ICAR6---------------------------
DRG2 =  None
CEC2 = None
CAT2 = None
SIAV2 = None
DBNB2 = None
DIA2 = None
CREAT2 = None
DCREAT2 = None
BILI2 = None
DBILI2 = None
BILI_AVI = None
DIA_AVI = None
CRE_AVI = None
BNP_AVI = None
PBN_AVI = None
PROBNP = None
BNP = None

scoreICAR = getICAR()
F_ICAR = 1000 * ICAR / 40

urgence = None
fICAR = None
XPC = None
F_ICAR = None
KXPC = None
DAURG = None
DA = None
KXPC = None
DAURG = None

ScoreCCB = getCCB(CAS, XPCA, CPS, XPCP)

MAL = None
MAL2 = None
MAL3 = None
BILI = None
dateDBILI = None
dVarBio = None
LnDFG = None
DFG = None
ABOD = None
ABOR= None
tailleD = None
tailleR = None
poidsD = None
poidsR = None

ScoreCCP = getScoreCCP(CCB, ABO, SC, )

NAGC = getScoreNACG()