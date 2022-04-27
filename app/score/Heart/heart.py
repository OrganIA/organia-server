import numpy as np
from scoreICAR import getICAR
from scoreCCP import getScoreCCP
from scoreCCB import getScoreCCB
from datetime import datetime
from test import sample1


class Model:
    def __init__(self, data):
        self.ageR = data['D_INSC'].year - data['R_D_NAI'].year
        self.ageD = data['D_INSC'].year - data['R_D_NAI'].year
        self.sexD = data['SEXD']
        self.sexR = data['SEXR']
        self.tailleD = data['TAILLED']
        self.tailleR = data['TAILLER']
        self.poidsD = data['POIDSD']
        self.poidsR = data['POIDSR']

        self.DRG = data['DRG']
        self.CEC = data['CEC']
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
        self.Date_Courante = datetime.now()
        self.DelaiVarBioGRF = getDelaiVarBioGRF(self.CEC, self.DRG)
        self.DPROBNB = data['DPROBNP']
        self.BNP = data['BNP']

        self.urgence = data['URGENCE']
        self.XPC = data['XPC']
        self.KXPC = data['KXPC']
        self.DAURG = (data['D_PREL'].year - data['D_URGENCE'].year) * 12 + (data['D_PREL'].month - data['D_URGENCE'].month)
        self.DA = (data['D_PREL'].year - data['D_INSC'].year) * 12 + (data['D_PREL'].month - data['D_INSC'].month)

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
    MG = 1 / np.exp(0.00000002 * pow(TTLGP, 2.9))
    return scoreCCP * MG


# ***********************************************************
model = Model(sample1)

scoreICAR = getICAR(model)
F_ICAR = 1000 * scoreICAR / 40
scoreCCB = getScoreCCB(model, F_ICAR)
scoreCCP = getScoreCCP(model, scoreCCB)
NAGC = getScoreNACG(scoreCCP, model.TTLGP)
