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

#Composante Expert Adulte -> XPCA
def getXPCA(ageR, urgence, XPC, fICAR, KXPC, DAURG):
    if ageR >= 18 and urgence == 'XPCA':
        if XPC == 0:
            return max(fICAR, KXPC)
        else:
            return max(fICAR, KXPC * max(0, min(1, DAURG/XPC)))
    else:
        return 0

def checkXPCA(XPCA):
    if XPCA > 900:
        raise Exception ("La composante XPCA ne peut depasser 900 points")
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

def getScoreCCB(CAS, XPCA, CPS, XPCP):
    return (CAS + XPCA + CPS + XPCP)