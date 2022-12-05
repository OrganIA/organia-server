import enum
from cmath import isnan
from datetime import datetime
from math import ceil as round

import numpy as np
import sqlalchemy as sa
from numpy import log as ln

from app import db
from app.helpers.enums import EnumStr


class Heart(db.Base):
    class URGENCE(EnumStr):
        XPCA = enum.auto()
        XPCP1 = enum.auto()
        XPCP2 = enum.auto()
        NA = enum.auto()

    listing_id = sa.Column(sa.ForeignKey('listings.id'))
    taille_D = sa.Column(sa.Float, nullable=True)
    poids_D = sa.Column(sa.Float, nullable=True)
    ABO_D = sa.Column(sa.String, nullable=True)
    sex_D = sa.Column(sa.String, nullable=True)
    R_D_NAI = sa.Column(sa.Date, nullable=True)
    D_INSC = sa.Column(sa.Date, nullable=True)
    MAL = sa.Column(sa.String, nullable=True)
    MAL2 = sa.Column(sa.String, nullable=True)
    MAL3 = sa.Column(sa.String, nullable=True)
    urgence = sa.Column(sa.Enum(URGENCE), nullable=True)
    d_urgence = sa.Column(sa.Date, nullable=True)
    KXPC = sa.Column(sa.String, nullable=True)
    XPC = sa.Column(sa.Integer, nullable=True)
    DRG = sa.Column(sa.String, nullable=True)
    CEC = sa.Column(sa.String, nullable=True)
    DCEC = sa.Column(sa.Date, nullable=True)
    SIAV = sa.Column(sa.String, nullable=True)
    CAT = sa.Column(sa.String, nullable=True)
    BNP = sa.Column(sa.Integer, nullable=True)
    DBNP = sa.Column(sa.Integer, nullable=True)
    PROBNP = sa.Column(sa.Float, nullable=True)
    DPROBNP = sa.Column(sa.Date, nullable=True)
    DIA = sa.Column(sa.String, nullable=True)
    CREAT = sa.Column(sa.Float, nullable=True)
    DCREAT = sa.Column(sa.Date, nullable=True)
    BILI = sa.Column(sa.Float, nullable=True)
    DBILI = sa.Column(sa.Date, nullable=True)
    BNP_AVI = sa.Column(sa.Float, nullable=True)
    PBN_AVI = sa.Column(sa.Float, nullable=True)
    DIA_AVI = sa.Column(sa.String, nullable=True)
    CRE_AVI = sa.Column(sa.Float, nullable=True)
    BILI_AVI = sa.Column(sa.Float, nullable=True)
    TTLGP = sa.Column(sa.Float, nullable=True)
    ICAR = sa.Column(sa.Float, nullable=True)
    F_ICAR = sa.Column(sa.Float, nullable=True)
    comp_ad_std = sa.Column(sa.Float, nullable=True)
    comp_ad_XPCA = sa.Column(sa.Float, nullable=True)
    comp_ped_std = sa.Column(sa.Float, nullable=True)
    comp_ped_XPCP = sa.Column(sa.Float, nullable=True)
    score_CCB = sa.Column(sa.Float, nullable=True)
    F1_dif_age = sa.Column(sa.Boolean, nullable=True)
    F2_ABO = sa.Column(sa.Boolean, nullable=True)
    F3_SC = sa.Column(sa.Boolean, nullable=True)
    F4_surv_post_GRF = sa.Column(sa.Boolean, nullable=True)
    score_CCP = sa.Column(sa.Float, nullable=True)
    score_NACG = sa.Column(sa.Float, nullable=True)
    D_D_NAI = sa.Column(sa.Date, nullable=True)
    D_PREL = sa.Column(sa.Date, nullable=True)
    score = sa.Column(sa.Float, nullable=True, default=0)

    def get_delai_var_bio_GRF(self, CEC, DRG):
        if CEC != 'O' and DRG != 'O':
            return 105
        else:
            return 4

    def get_score_NACG(self, score_CCP, TTLGP):
        MG = 1 / np.exp(0.0000002 * pow(TTLGP, 2.9))
        return score_CCP * MG

    def get_CAS(self, age_R, urgence, fICAR):
        if age_R >= 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
            if fICAR < 775:
                return fICAR
            else:
                return fICAR + 51
        else:
            return 0

    def check_CAS(self, CAS):
        if CAS < 0 or (CAS > 775 and CAS < 826) or CAS > 1051:
            raise Exception(
                "La composante adulte standard doit se situer entre 0 et 775\n"
                "points ou 826 et 1051 points"
            )
        else:
            return 0

    def get_XPCA(self, age_R, urgence, XPC, fICAR, KXPC, DAURG):
        if age_R >= 18 and urgence == 'XPCA':
            if XPC == 0:
                return max(fICAR, KXPC)
            else:
                return max(fICAR, KXPC * max(0, min(1, DAURG / XPC)))
        else:
            return 0

    def check_XPCA(self, XPCA):
        if XPCA != 900:
            raise Exception(
                "La composante XPCA ne peut etre differente de 900 points"
            )
        else:
            return 0

    def get_CPS(self, age_R, urgence, DA):
        if age_R < 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
            return 775 + 50 * max(0, min(1, DA / 24))
        else:
            return 0

    def check_CPS(self, CPS):
        if CPS < 776 or CPS > 825:
            raise Exception(
                "La composante pediatrique standard doit se situer entre 776\
                et 825 points"
            )
        else:
            return 0

    def get_XPCP(self, urgence, KXPC, DAURG):
        if urgence == 'XPCP1' or urgence == 'XPCP2':
            return KXPC + 50 * max(0, min(1, DAURG / 24))
        else:
            return 0

    def check_XPCP(self, urgence, XPCP):
        if urgence == 'XPCP1' and XPCP < 1102 or XPCP > 1151:
            raise Exception(
                "Le score XPCP pour une urgence de niveau 1 doit se situer\
                     entre 1102 et 1151 points"
            )
        elif urgence == 'XPCP2' and XPCP < 1051 or XPCP > 1101:
            raise Exception(
                "Le score XPCP pour une urgence de niveau 2 doit se situer\
                    entre 1051 et 1101 points"
            )
        else:
            return 0

    # def getScoreCCB(self, F_ICAR):
    #     CAS = self.get_CAS(self.age_R, self.urgence, F_ICAR)
    #     XPCA = self.get_XPCA(self.age_R, self.urgence,
    #                         self.XPC, F_ICAR, self.KXPC, self.DAURG)
    #     CPS = self.get_CPS(self.age_R, self.urgence, self.DA)
    #     XPCP = self.get_XPCP(self.urgence, self.KXPC, self.DAURG)
    #     return (CAS + XPCA + CPS + XPCP)

    def get_dif_age(self, age_R, age_D):
        ageRD = age_R - age_D
        dif_age = 0

        if ageRD < 0:
            dif_age = (ageRD + 65) / 25
        else:
            dif_age = 1 - (ageRD - 15) / 25
        if age_R >= 18:
            dif_age = min(1, max(0, dif_age))
        else:
            dif_age = 1
        return dif_age

    def get_ABO(self, ABO_D, ABOR):
        if (
            (ABO_D == ABOR)
            or (ABO_D == 'A' and ABOR == 'AB')
            or (ABO_D == 'O' and ABOR == 'B')
        ):
            return 1
        elif ABO_D == 'O' and ABOR == 'AB':
            return 0.1
        else:
            return 0

    def get_SC(self, taille_D, taille_R, poids_D, poids_R, age_R, sex_D):
        fscD = 0.007184 * (pow(taille_D, 0.725)) * (pow(poids_D, 0.425))
        fscR = 0.007184 * (pow(taille_R, 0.725)) * (pow(poids_R, 0.425))

        if age_R >= 18:
            if 0.8 * fscR < fscD or (sex_D == 'MALE' and poids_D >= 70):
                return 1
            else:
                return 0
        else:
            if (0.8 * fscR < fscD and 2 * fscR > fscD) or (
                sex_D == 'MALE' and poids_D >= 70
            ):
                return 1
            else:
                return 0

    def get_surv_post_GRF(self, risk_post_GRF):
        return pow(0.6785748856, np.exp(risk_post_GRF))

    def tri_surv_post_GRF(self, surv_post_GRF, age_R):
        if surv_post_GRF > 0.5 or age_R < 18:
            return 1
        else:
            return 0

    def get_risk_post_GRF(self, fage_R, fage_D, f_MAL, LnBili, LnDFG, sex_RD):
        return (
            0.50608 * fage_R
            + 0.50754 * f_MAL
            + 0.40268 * LnBili
            - 0.54443 * LnDFG
            + 0.36262 * sex_RD
            + 0.41714 * fage_D
        )

    def get_f_age_r(self, age_R):
        if age_R > 50:
            return 1
        else:
            return 0

    def get_f_MAL(self, MAL, MAL2, MAL3):
        mal = [
            'Maladie valvulaire',
            'Maladie congenitale',
            'Maladie congenitale non Eisenmenger',
        ]
        if MAL in mal or MAL2 in mal or MAL3 in mal:
            return 1
        else:
            return 0

    def get_LnBili(self, BILI, date_DBILI, d_var_bio, date_courante):
        x = np.timedelta64((date_courante - date_DBILI), 'ns')
        day = x.astype('timedelta64[D]')
        date_DBILI = day.astype(int)

        if np.isnan(BILI) is True or date_DBILI > d_var_bio:
            return np.log(230)
        else:
            return np.log(min(230, max(5, BILI)))

    def get_LnDFG(self, DIA, CREAT, DCREAT, d_var_bio, DFG, date_courante):
        x = np.timedelta64((date_courante - DCREAT), 'ns')
        day = x.astype('timedelta64[D]')
        DCREAT = day.astype(int)

        if DIA == 'O':
            return np.log(15)
        elif np.isnan(CREAT) is True or DCREAT > d_var_bio:
            return np.log(1)
        else:
            return np.log(min(150, max(1, DFG)))

    # Fonction sur l’appariemment du sexe entre donneur et receveur

    def get_sex_RD(self, sex_D, sex_R):
        if sex_D == 'MALE' and sex_R == 'FEMALE':
            return 1
        else:
            return 0

    # Fonction sur l’âge du donneur

    def get_f_ageD(self, age_D):
        if age_D > 55:
            return 1
        else:
            return 0

    # Fonction Débit de Filtration Glomérulaire en Liste d’attente \
    # (méthode MDRD) du jour

    def get_d_dfgj(self, sex_R, age_R, CREAT):
        if sex_R == 'FEMALE':
            return (
                186.3
                * (pow((CREAT / 88.4), -1.154))
                * (pow(age_R, -0.203))
                * 0.742
            )
        else:
            return (
                186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(age_R, -0.203)) * 1
            )

    # ********************Score CCP******************

    def get_score_CCP(self, CCB):
        F_DFGj = self.get_d_dfgj(self.sex_R, self.age_R, self.CREAT)
        LnDFG = self.get_LnDFG(
            self.DIA,
            self.CREAT,
            self.DCREAT,
            self.delai_var_bio_GRF,
            F_DFGj,
            self.date_courante,
        )
        fage_D = self.get_f_ageD(self.age_D)
        sex_RD = self.get_sex_RD(self.sex_D, self.sex_R)
        LnBili = self.get_LnBili(
            self.BILI,
            self.date_DBILI,
            self.delai_var_bio_GRF,
            self.date_courante,
        )
        f_MAL = self.get_f_MAL(self.MAL, self.MAL2, self.MAL3)
        fage_R = self.get_f_age_r(self.age_R)
        risk_post_GRF = self.get_risk_post_GRF(
            fage_R, fage_D, f_MAL, LnBili, LnDFG, sex_RD
        )
        dif_age = self.get_dif_age(self.age_R, self.age_D)
        ABO = self.get_ABO(self.ABO_D, self.ABOR)
        SC = self.get_SC(
            self.taille_D,
            self.taille_R,
            self.poids_D,
            self.poids_R,
            self.age_R,
            self.sex_D,
        )
        surv_post_GRF = self.get_surv_post_GRF(risk_post_GRF)
        tri_surv_post_grf = self.tri_surv_post_GRF(surv_post_GRF, self.age_R)
        return CCB * dif_age * ABO * SC * tri_surv_post_grf

    # ***********************************************

    # Index de risque Cardiaque du jour (ICARj)

    # Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) du jour

    def get_f_decile_pnj(
        self,
        CEC,
        CAT,
        SIAV,
        DBNP,
        BNP,
        PROBNP,
        date_courante,
        DPROBNP,
        delai_var_bio_LA,
    ):
        if CEC == 'O' or CAT == 'O' or SIAV == 'B':
            return 10
        elif isnan(BNP) is True and isnan(PROBNP) is True:
            return 1
        elif (
            isnan(PROBNP) is not True
            and (date_courante - DPROBNP).days <= delai_var_bio_LA
        ):
            conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
            res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if PROBNP >= 11332:
                return 10
            for index, condition in enumerate(conditions):
                if PROBNP < condition:
                    return res[index]
        elif (
            isnan(BNP) is not True
            and (date_courante - DBNP).days <= delai_var_bio_LA
        ):
            conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
            res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if BNP >= 2696:
                return 10
            for index, condition in enumerate(conditions):
                if BNP < condition:
                    return res[index]
        else:
            return 1

    def get_F_Ln_DFG_LAj(
        self, DIA, CREAT, DCREAT, sex_R, age_R, date_courante, delai_var_bio_LA
    ):
        F_DFGj = self.get_d_dfgj(sex_R, age_R, CREAT)
        if DIA == 'O':
            return ln(15)
        elif (
            isnan(CREAT) is True
            or (date_courante - DCREAT).days > delai_var_bio_LA
        ):
            return ln(150)
        else:
            return ln(min(150, max(1, F_DFGj)))

    # Fonction Bilirubine en Liste d’attente du jour

    def getF_Ln_BILI_LAj(self, BILI, DBILI, date_courante, delai_var_bio_LA):
        if (
            isnan(BILI) is True
            or (date_courante - DBILI).days > delai_var_bio_LA
        ):
            return ln(5)
        else:
            return ln(min(230, max(5, BILI)))

    # Fonction Assistance de Courte Durée

    def get_f_ASCD(self, CEC):
        if CEC == 'O':
            return 1
        else:
            return 0

    # La fonction de risque pré-greffe en liste d’attente du jour

    def get_f_risque_pre_GRFj(
        self, F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj
    ):
        return (
            1.301335 * F_ASCD
            + 0.157691 * F_Decile_PNj
            - 0.510058 * F_Ln_DFG_LAj
            + 0.615711 * F_Ln_BILI_LAj
        )

    # La function Index de risque Cardiaque du jour (ICARj)

    def getICARj(self, F_RisquePreGRFj, C_ICAR):
        return min(40, max(0, round((F_RisquePreGRFj - C_ICAR) * 10)))

    # ----------------------

    # Index de risque avant perfusion ou implantation CEC (ICARi)

    # Fonction Décile des peptides natriurétiques (BNP ou NT-ProBNP) initiale

    def get_F_decile_PNi(self, BNP_AVI, PBN_AVI, PROBNP, BNP, CEC, CAT, SIAV):
        if CEC == 'O' or CAT == 'O' or SIAV == 'B':
            return 10
        elif isnan(BNP_AVI) is True and isnan(PBN_AVI) is True:
            return 1
        elif isnan(PBN_AVI) is not True:
            conditions = [928, 1478, 2044, 2661, 3416, 4406, 5645, 8000, 11332]
            res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if PROBNP >= 11332:
                return 10
            for index, condition in enumerate(conditions):
                if PROBNP < condition:
                    return res[index]
        elif isnan(BNP_AVI) is not True:
            conditions = [189, 314, 481, 622, 818, 1074, 1317, 1702, 2696]
            res = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            if BNP >= 2696:
                return 10
            for index, condition in enumerate(conditions):
                if BNP < condition:
                    return res[index]
        else:
            return 1

    # Fonction Débit de Filtration Glomérulaire en Liste d’attente \
    # (méthode MDRD) initiale

    def get_f_DFGi(self, sex_R, CRE_AVI, age_R):
        if sex_R == 'FEMALE':
            return (
                186.3
                * ((CRE_AVI / 88.4) * -1.154)
                * (pow(age_R, -0.203))
                * 0.742
            )
        else:
            return (
                186.3 * ((CRE_AVI / 88.4) * -1.154) * (pow(age_R, -0.203)) * 1
            )

    def get_f_Ln_DFG_LAi(self, DIA_AVI, CRE_AVI, sex_R, age_R):
        F_DFGi = self.get_f_DFGi(sex_R, CRE_AVI, age_R)
        if DIA_AVI == 'O':
            return ln(15)
        elif isnan(CRE_AVI) is True:
            return ln(150)
        else:
            return ln(min(150, max(1, F_DFGi)))

    # Fonction Bilirubine en Liste d’attente initiale

    def get_f_Ln_BILI_LAi(self, BILI_AVI):
        if isnan(BILI_AVI) is True:
            return ln(5)
        else:
            return ln(min(230, max(5, BILI_AVI)))

    # La fonction de risque pré-greffe en liste d’attente initiale

    def get_f_risque_pre_GRFi(
        self, F_ASCD, F_decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi
    ):
        return (
            1.301335 * F_ASCD
            + 0.157691 * F_decile_PNi
            - 0.510058 * F_Ln_DFG_LAi
            + 0.615711 * F_Ln_BILI_LAi
        )

    # Index de risque avant perfusion ou implantation CEC (ICARi)

    def get_ICARi(self, F_risque_pre_GRFi, C_ICAR):
        return min(40, max(0, round((F_risque_pre_GRFi - C_ICAR) * 10)))

    # -------------------------------------

    # ---------Calcul de l’Index de Risque Cardiaque (ICAR)

    def get_ICAR(self, sex_R, age_R):
        date_courante = datetime.utcnow().date()
        delai_var_bio_GRF = 30
        if self.CREAT <= 0:
            self.CREAT += 10
        C_ICAR = (
            1.301335 * 0 + 0.157691 * 1 - 0.510058 * ln(150) + 0.615711 * ln(5)
        )
        F_Decile_PNj = self.get_f_decile_pnj(
            self.CEC,
            self.CAT,
            self.SIAV,
            self.DBNP,
            self.BNP,
            self.PROBNP,
            date_courante,
            self.DPROBNP,
            delai_var_bio_GRF,
        )
        F_Ln_DFG_LAj = self.get_F_Ln_DFG_LAj(
            self.DIA,
            self.CREAT,
            self.DCREAT,
            sex_R,
            age_R,
            date_courante,
            delai_var_bio_GRF,
        )
        F_Ln_BILI_LAj = self.getF_Ln_BILI_LAj(
            self.BILI, self.DBILI, date_courante, delai_var_bio_GRF
        )
        F_ASCD = self.get_f_ASCD(self.CEC)
        F_RisquePreGRFj = self.get_f_risque_pre_GRFj(
            F_ASCD, F_Decile_PNj, F_Ln_DFG_LAj, F_Ln_BILI_LAj
        )
        ICARj = self.getICARj(F_RisquePreGRFj, C_ICAR)

        F_Ln_BILI_LAi = self.get_f_Ln_BILI_LAi(self.BILI_AVI)
        F_Ln_DFG_LAi = self.get_f_Ln_DFG_LAi(
            self.DIA_AVI, self.CRE_AVI, sex_R, age_R
        )
        F_decile_PNi = self.getF_Decile_PNi(
            self.BNP_AVI,
            self.PBN_AVI,
            self.PROBNP,
            self.BNP,
            self.CEC,
            self.CAT,
            self.SIAV,
        )
        F_risque_pre_GRFi = self.get_f_risque_pre_GRFi(
            F_ASCD, F_decile_PNi, F_Ln_DFG_LAi, F_Ln_BILI_LAi
        )
        ICARi = self.get_ICARi(F_risque_pre_GRFi, C_ICAR)

        if self.CEC != 'O' and self.DRG != 'O':
            return ICARj
        else:
            return max(ICARj, ICARi)

    def check_ICAR(self, ICAR):
        if ICAR > 40 or ICAR < 0:
            raise Exception("Le score ICAR doit etre compris entre 0 et 40")
        else:
            return ICAR
