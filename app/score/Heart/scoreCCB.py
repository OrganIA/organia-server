from logging import exception
from numpy import log as ln

#Composant Adulte Standard -> CAS
def getCAS(ageR, urgence, fICAR):
    if ageR >= 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
        if fICAR < 775:
            return fICAR
        else:
            return fICAR + 51
    else:
        return 0
#verification de la CAS
def checkCAS(CAS):
    if CAS < 0 or (CAS > 775 and CAS < 826) or CAS > 1051:
        raise Exception ("La composante adulte standard doit se situer entre 0 et 775 points ou 826 et 1051 points")
    else:
        return 0

#Composante Expert Adulte -> XPCA
def getXPCA(ageR, urgence, XPC, fICAR, KXPC, DAURG):
    if ageR >= 18 and urgence == 'XPCA':
        if XPC == 0:
            return max(fICAR, KXPC)
        else:
            return max(fICAR, KXPC * max(0, min(1, DAURG/XPC)))
    else:
        return 0

# Verification de la XPCA
def checkXPCA(XPCA):
    if XPCA != 900:
        raise Exception ("La composante XPCA ne peut etre differente de 900 points")
    else:
        return 0
        
#Composante Pédiatrique Standard -> CPS
def getCPS(ageR, urgence, DA):
    if ageR < 18 and urgence not in  ['XPCA', 'XPCP1', 'XPCP2']:
        return (775 + 50 * max(0, min(1, DA / 24)))
    else:
        return 0
#Composante Expert Pédiatrique -> XPCP
def getXPCP(urgence, KXPC, DAURG):
    if urgence == 'XPCP1' or urgence == 'XPCP2':
        return (KXPC + 50 * max(0, min(DAURG / 24)))
    else:
        return 0

def getScoreCCB(model, F_ICAR):
    CAS = getCAS(model.ageR, model.urgence, F_ICAR)
    XPCA = getXPCA(model.ageR, model.urgence, model.XPC, F_ICAR, model.KXPC, model.DAURG)
    CPS = getCPS(model.ageR, model.urgence, model.DA)
    XPCP = getXPCP(model.urgence, model.KXPC, model.DAURG)
    return (CAS + XPCA + CPS + XPCP)
