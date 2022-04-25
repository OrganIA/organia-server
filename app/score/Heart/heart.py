from random import sample
from sqlite3 import Timestamp
from xml.dom.domreg import well_known_implementations
import numpy as np
from scoreICAR import getICAR
from scoreCCP import getScoreCCP
from scoreCCB import getScoreCCB
from datetime import datetime, timedelta
from test import sample1

class Model:
    def __init__(self, data):
        self.ageR = round((data['D_INSC'] - data['R_D_NAI']).days / 365)
        self.ageD = round((data['D_INSC'] - data['R_D_NAI']).days / 365)
        self.sexD = data['SEXD']
        self.sexR = data['SEXR']
        self.tailleD = data['TAILLED']
        self.tailleR = data['TAILLER']
        self.poidsD = data['POIDSD']
        self.poidsR = data['POIDSR']

        self.DRG =  data['DRG']
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
        self.DAURG = data['D_PREL'] - data['D_URGENCE']
        self.DA = data['D_PREL'] - data['D_INSC']

        self.MAL = data['MAL']
        self.MAL2 = data['MAL2']
        self.MAL3 = data['MAL3']
        self.BILI = data['BILI']
        self.dateDBILI = data['DBILI']
        self.ABOD = data['ABOD']
        self.ABOR = data['ABOR']
        self.TTLGP = data['TTLGP']
        self.DBNP = data['DBNP']
#----------------------------------------------------------------------
        #self.D_INSC
        #self.D_URGENCE
        #self.Delai_URGENCE
        #self.D_CEC
        #self.D_BNP
        #self.DISTANCE
        #self.Kequipe
#-----------------------------------------------------------------------
        self.F_DFG = 0
        # self.ABOD
        # self.ABOR
        # self.TTLGP
        # self.XPC
        # self.KXPC
        # self.DAURG
        # self.DA


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