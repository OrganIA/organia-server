import numpy as np
from scoreICAR import getICAR
from scoreCCP import getScoreCCP
from scoreCCB import getScoreCCB

class Model:
    def __init__(self):
        self.ageR = 0
        self.ageD = 0
        self.sexD = 0
        self.sexR = 0
        self.tailleD = 0
        self.tailleR = 0
        self.poidsD = 0
        self.poidsR = 0

        self.DRG2 =  0
        self.CEC2 = 0
        self.CAT2 = 0
        self.SIAV2 = 0
        self.DBNB2 = 0
        self.DIA2 = 0
        self.CREAT2 = 0
        self.DCREAT2 = 0
        self.BILI2 = 0
        self.DBILI2 = 0
        self.BILI_AVI = 0
        self.DIA_AVI = 0
        self.CRE_AVI = 0
        self.BNP_AVI = 0
        self.PBN_AVI = 0
        self.PROBNP = 0
        self.BNP = 0

        self.urgence = 0
        self.XPC = 0
        self.KXPC = 0
        self.DAURG = 0
        self.DA = 0

        self.MAL = 0
        self.MAL2 = 0
        self.MAL3 = 0
        self.BILI = 0
        self.dateDBILI = 0
        self.dVarBio = 0
        self.DFG = 0
        self.ABOD = 0
        self.ABOR= 0
        self.TTLGP= 0

# ************************Score NACG*************************


def getScoreNACG(scoreCCP, TTLGP):
    MG = 1 / np.exp(0.00000002 * TTLGP^2.9)
    return scoreCCP * MG

# ***********************************************************

model = Model()

scoreICAR = getICAR(model)
F_ICAR = 1000 * scoreICAR / 40
scoreCCB = getScoreCCB(model, F_ICAR)
scoreCCP = getScoreCCP(model)
NAGC = getScoreNACG(scoreCCP, model.TTLGP)