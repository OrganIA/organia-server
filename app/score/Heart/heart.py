from random import sample
from sqlite3 import Timestamp
import numpy as np
from pandas import Timedelta
from scoreICAR import getICAR
from scoreCCP import getScoreCCP
from scoreCCB import getScoreCCB
from datetime import datetime
from test import sample1


class Model:
    def __init__(self, data):
        self.ageR = data['R_D_NAI'] - Timedelta
        self.ageD = data['D_D_NAI'] - Timedelta
        self.sexD = data['sexD']
        self.sexR = data['SexR']
        self.tailleD = data['tailleD']
        self.tailleR = data['tailleR']
        self.poidsD = data['poidD']
        self.poidsR = data['poidR']

        self.DRG =  data['DRG']
        self.CEC = data['CEC']
        self.CAT = data['CAT']
        self.SIAV = data['SIAV']
        self.DBNB = 0
        self.DIA = data['DIA']
        self.CREAT = data['CREAT']
        self.DCREAT = data['DCREAT']
        # self.BILI2 = 0
        self.DBILI = data['DBILI']
        self.BILI_AVI = data['BILI_AVI']
        self.DIA_AVI = data['DIA_AVI']
        self.CRE_AVI = data['CRE_AVI']
        self.BNP_AVI = data['BNP_AVI']
        self.PBN_AVI = data['PBN_AVI']
        # self.PROBNP2 = 0
        self.PROBNP = data['PROBNP']
        self.Date_Courante = Timedelta
        self.DPROBNB = data['DPROBNP']
        self.Delai_Var_Bio_LA = Timedelta
        self.BNP = data['BNP']
        # self.BNP2 = 0

        self.urgence = data['URGENCE']
        self.XPC = 0
        self.KXPC = 0
        self.DAURG = 0
        self.DA = 0

        self.MAL = data['MALADIE 1']
        self.MAL2 = data['MALADIE 2']
        self.MAL3 = data['MALADIE 3']
        self.BILI = data['BILI']
        self.dateDBILI = data['DBILI']
        self.dVarBio = datetime.now()
        self.DFG = 0
        self.ABOD = 0
        self.ABOR= 0
        self.TTLGP= 0

# ************************Score NACG*************************

print(type(sample1['DPROBNP']), )
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