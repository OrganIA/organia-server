import numpy as np
from score.Heart.scoreICAR import getICAR
from score.Heart.scoreCCP import getScoreCCP
from score.Heart.scoreCCB import getScoreCCB

class Model:
    def __init__(self):
        self.ageR = None
        self.ageD = None
        self.sexD = None
        self.sexR = None
        self.tailleD = None
        self.tailleR = None
        self.poidsD = None
        self.poidsR = None

        self.DRG2 =  None
        self.CEC2 = None
        self.CAT2 = None
        self.SIAV2 = None
        self.DBNB2 = None
        self.DIA2 = None
        self.CREAT2 = None
        self.DCREAT2 = None
        self.BILI2 = None
        self.DBILI2 = None
        self.BILI_AVI = None
        self.DIA_AVI = None
        self.CRE_AVI = None
        self.BNP_AVI = None
        self.PBN_AVI = None
        self.PROBNP = None
        self.BNP = None

        self.urgence = None
        self.XPC = None
        self.KXPC = None
        self.DAURG = None
        self.DA = None

        self.MAL = None
        self.MAL2 = None
        self.MAL3 = None
        self.BILI = None
        self.dateDBILI = None
        self.dVarBio = None
        self.DFG = None
        self.ABOD = None
        self.ABOR= None
        self.TTLGP= None

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