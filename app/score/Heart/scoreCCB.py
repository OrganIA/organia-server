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
    return
#Composante Expert Pédiatrique -> XPCP
def getXPCP(urgence, KXPC, DAURG):
    return

def getCCB(CAS, XPCA, CPS, SCXP):
    return