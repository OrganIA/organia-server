import datetime
import logging

import numpy as np

from app.db.models import Heart, Person


def get_CAS(age_R, urgence, fICAR):
    if age_R >= 18 and urgence == Heart.EMERGENCY.NA:
        if fICAR < 775:
            return fICAR
        else:
            return fICAR + 51
    else:
        return 0


def get_XPCA(age_R, urgence, XPC, fICAR, KXPC, DAURG):
    if age_R >= 18 and urgence == Heart.EMERGENCY.XPCA:
        if XPC == 0:
            return max(fICAR, KXPC)
        else:
            return max(fICAR, KXPC * max(0, min(1, DAURG / XPC)))
    else:
        return 0


def get_CPS(age_R, urgence, DA):
    if age_R < 18 and urgence not in ['XPCA', 'XPCP1', 'XPCP2']:
        return 775 + 50 * max(0, min(1, DA / 24))
    else:
        return 0


def get_XPCP(urgence, KXPC, DAURG):
    if urgence in (Heart.EMERGENCY.XPCP1, Heart.EMERGENCY.XPCP2):
        return KXPC + 50 * max(0, min(1, DAURG / 24))
    else:
        return 0


def getScoreCCB(receiver):
    CAS = get_CAS(
        receiver.person.age, receiver.organ.emergency, receiver.organ.F_ICAR
    )
    XPCA = get_XPCA(
        receiver.person.age,
        receiver.organ.emergency,
        receiver.organ.XPC,
        receiver.organ.F_ICAR,
        receiver.organ.KXPC,
        receiver.organ.DAURG,
    )
    CPS = get_CPS(
        receiver.person.age, receiver.organ.emergency, receiver.organ.DA
    )
    XPCP = get_XPCP(
        receiver.organ.emergency, receiver.organ.KXPC, receiver.organ.DAURG
    )
    return CAS + XPCA + CPS + XPCP


def get_dif_age(age_R, age_D):
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


def get_ABO(ABO_D, ABOR):
    if (
        (ABO_D == ABOR)
        or (ABO_D == Person.ABO.A and ABOR == Person.ABO.AB)
        or (ABO_D == Person.ABO.O and ABOR == Person.ABO.B)
    ):
        return 1
    if ABO_D == 'O' and ABOR == 'AB':
        return 0.1
    return 0


def get_SC(taille_D, taille_R, poids_D, poids_R, age_R, sex_D):
    fscD = 0.007184 * (pow(taille_D, 0.725)) * (pow(poids_D, 0.425))
    fscR = 0.007184 * (pow(taille_R, 0.725)) * (pow(poids_R, 0.425))

    if age_R >= 18:
        if 0.8 * fscR < fscD or (sex_D == Person.Gender.MALE and poids_D >= 70):
            return 1
        return 0

    if (0.8 * fscR < fscD and 2 * fscR > fscD) or (
        sex_D == 'MALE' and poids_D >= 70
    ):
        return 1
    return 0


def get_surv_post_GRF(risk_post_GRF):
    return pow(0.6785748856, np.exp(risk_post_GRF))


def tri_surv_post_GRF(surv_post_GRF, age_R):
    if surv_post_GRF > 0.5 or age_R < 18:
        return 1
    return 0


def get_risk_post_GRF(fage_R, fage_D, f_MAL, LnBili, LnDFG, sex_RD):
    return (
        0.50608 * fage_R
        + 0.50754 * f_MAL
        + 0.40268 * LnBili
        - 0.54443 * LnDFG
        + 0.36262 * sex_RD
        + 0.41714 * fage_D
    )


def get_f_age_r(age_R):
    if age_R > 50:
        return 1
    return 0


def get_f_MAL(MAL, MAL2, MAL3):
    if any(x is not None for x in [MAL, MAL2, MAL3]):
        return 1
    return 0


def get_LnBili(BILI, date_DBILI, d_var_bio, date_courante):
    x = np.timedelta64((date_courante - date_DBILI), 'ns')
    day = x.astype('timedelta64[D]')
    date_DBILI = day.astype(int)

    if np.isnan(BILI) or date_DBILI > d_var_bio * (24 * 60 * 60):
        return np.log(230)
    return np.log(min(230, max(5, BILI)))


def get_LnDFG(DIA, CREAT, DCREAT, d_var_bio, DFG, date_courante):
    x = np.timedelta64((date_courante - DCREAT), 'ns')
    day = x.astype('timedelta64[D]')
    DCREAT = day.astype(int)

    if DIA:
        return np.log(15)
    if np.isnan(CREAT) or DCREAT > d_var_bio:
        return np.log(1)
    return np.log(min(150, max(1, DFG)))


# Fonction sur l’appariemment du sexe entre donneur et receveur


def get_sex_RD(sex_D, sex_R):
    if sex_D != sex_R:
        return 1
    return 0


# Fonction sur l’âge du donneur


def get_f_ageD(age_D):
    if age_D > 55:
        return 1
    return 0


# Fonction Débit de Filtration Glomérulaire en Liste d’attente \
# (méthode MDRD) du jour


def get_d_dfgj(sex_R, age_R, CREAT):
    if sex_R == Person.Gender.FEMALE:
        return (
            186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(age_R, -0.203)) * 0.742
        )
    return 186.3 * (pow((CREAT / 88.4), -1.154)) * (pow(age_R, -0.203)) * 1


def compute_heart_score(
    donor_listing,
    receiver_listing,
):
    current_date = datetime.datetime.utcnow().date()
    F_DFGj = get_d_dfgj(
        receiver_listing.person.gender,
        receiver_listing.person.age,
        receiver_listing.organ.CREAT,
    )
    LnDFG = get_LnDFG(
        receiver_listing.organ.DIA_is_O,
        receiver_listing.organ.CREAT,
        receiver_listing.organ.DCREAT,
        receiver_listing.organ.delay_var_bio_GRF,
        F_DFGj,
        current_date,
    )
    fage_D = get_f_ageD(donor_listing.person.age)
    sex_RD = get_sex_RD(
        donor_listing.person.gender, receiver_listing.person.gender
    )
    LnBili = get_LnBili(
        receiver_listing.organ.BILI,
        receiver_listing.organ.DBILI,
        receiver_listing.organ.delay_var_bio_GRF,
        current_date,
    )
    f_MAL = get_f_MAL(
        receiver_listing.organ.MAL,
        receiver_listing.organ.MAL2,
        receiver_listing.organ.MAL3,
    )
    fage_R = get_f_age_r(receiver_listing.person.age)
    risk_post_GRF = get_risk_post_GRF(
        fage_R, fage_D, f_MAL, LnBili, LnDFG, sex_RD
    )
    dif_age = get_dif_age(
        receiver_listing.person.age, receiver_listing.person.age
    )
    ABO = get_ABO(donor_listing.person.abo, receiver_listing.person.abo)
    SC = get_SC(
        donor_listing.height_cm,
        receiver_listing.height_cm,
        donor_listing.weight_kg,
        receiver_listing.weight_kg,
        receiver_listing.person.age,
        donor_listing.person.gender,
    )
    surv_post_GRF = get_surv_post_GRF(risk_post_GRF)
    tri_surv_post_grf = tri_surv_post_GRF(
        surv_post_GRF, receiver_listing.person.age
    )
    CCB = getScoreCCB(receiver_listing)
    return (CCB * dif_age * ABO * SC * tri_surv_post_grf) / 5
