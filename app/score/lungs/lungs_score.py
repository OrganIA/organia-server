import decimal
import json
import logging
import math

from app import db
from app.db.models.lung import Lung
from app.errors import NotFoundError


def fetch_baseline_values(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data["data"]


def calculate_next_year_survival_chance_exponent(
    receiver, receiver_listing, listing_lung
):
    e = 0

    if (
        listing_lung.diagnosis_group == Lung.DiagnosisGroup.A
        or listing_lung.diagnosis_group == Lung.DiagnosisGroup.B
        or listing_lung.diagnosis_group == Lung.DiagnosisGroup.C
    ):
        e += receiver.age * 0.015097  # Age Today - Birthday
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.D:
        e += receiver.age * 0.021223  # Age
    e += listing_lung.body_mass_index * (-0.051781)  # Body Mass
    if listing_lung.diabetes:
        e += 0.158821
    if listing_lung.assistance_required:
        e += 0.115024
    else:
        e += 0.182250
    e += listing_lung.FVC_percentage * (-0.019675)  # FVC not sure about %
    if (
        listing_lung.diagnosis_group == Lung.DiagnosisGroup.A
        or listing_lung.diagnosis_group == Lung.DiagnosisGroup.D
        or listing_lung.diagnosis_group == Lung.DiagnosisGroup.C
    ):
        e += listing_lung.PA_systolic * 0.015889  # PA
    if (
        listing_lung.diagnosis_group == Lung.DiagnosisGroup.A
        or listing_lung.diagnosis_group == Lung.DiagnosisGroup.D
    ):
        e += (
            listing_lung.oxygen_requirement * 0.187599
        )  # 02 requirement at rest
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.B:
        e += (
            listing_lung.oxygen_requirement * 0.040766
        )  # 02 requirement at rest
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.C:
        e += (
            listing_lung.oxygen_requirement * 0.125568
        )  # 02 requirement at rest
    if listing_lung.six_minutes_walk_distance_over_150_feet:
        e += 0.330752
    if listing_lung.continuous_mech_ventilation:
        e += 1.213804
    e += (listing_lung.PCO2 - 40) * 0.005448  # PCO2
    if listing_lung.PCO2_increase_superior_to_15_percent:
        e += 0.076370
    if listing_lung.diagnosis_group == Lung.DiagnosisGroup.B:
        e += 2.376700
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.C:
        e += 0.943377
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.D:
        e += 0.996936
    if listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Bronchiectasis:
        e += 0.157212
    elif listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Eisenmenger:
        e += -0.627866
    elif (
        listing_lung.detailed_diagnosis
        == Lung.DetailedDiagnosis.Lymphangioleiomyomatosis
    ):
        e += -0.197434
    elif (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Bronchiolitis
    ):
        e += -0.256480
    if (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Sarcoidosis
        and receiver_listing.PA_systolic > 30
    ):
        e += -0.707346
    elif (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Sarcoidosis
        and receiver_listing.PA_systolic <= 30
    ):
        e += 0.455348
    return e


def next_year_survival_chance(receiver, receiver_listing, listing_lung):
    score = []

    exponent = calculate_next_year_survival_chance_exponent(
        receiver, receiver_listing, listing_lung
    )
    baseline_values = fetch_baseline_values(
        './data/lungs/BaselineWaitingListSurvival.json'
    )
    for baseline_value in baseline_values:
        baseline_value = decimal.Decimal(baseline_value)
        exponent = decimal.Decimal(exponent)
        score.append(baseline_value**exponent)
    return score


def calculate_post_transplant_survival_chance_exponent(
    receiver, receiver_listing, listing_lung
):
    e = 0

    if listing_lung.diagnosis_group == Lung.DiagnosisGroup.B:
        e += 0.623207
        e += listing_lung.FVC_percentage
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.C:
        e += 0.008514
    elif listing_lung.diagnosis_group == Lung.DiagnosisGroup.D:
        e += 0.413173
        e += listing_lung.FVC_percentage
        if listing_lung.PCW_over_20_mmHg:
            e += 0.033046

    e += listing_lung.age_at_transplant * 0.003510
    e += listing_lung.creatinine_at_transplant * 0.061986
    if listing_lung.ADL_required:
        e += -0.488525
    if listing_lung.continuous_mech_ventilation:
        e += 0.312846

    if listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Bronchiectasis:
        e += 0.056116
    elif listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Eisenmenger:
        e += 0.393526
    elif (
        listing_lung.detailed_diagnosis
        == Lung.DetailedDiagnosis.Lymphangioleiomyomatosis
    ):
        e += -0.624209
    elif (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Bronchiolitis
    ):
        e += -0.443786
    if (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Sarcoidosis
        and listing_lung.PA_systolic > 30
    ):
        e += -0.122351
    elif (
        listing_lung.detailed_diagnosis == Lung.DetailedDiagnosis.Sarcoidosis
        and listing_lung.PA_systolic <= 30
    ):
        e += -0.016505

    return e


def post_transplant_survival_chance(receiver, receiver_listing, listing_lung):
    score = []

    exponent = calculate_post_transplant_survival_chance_exponent(
        receiver, receiver_listing, listing_lung
    )
    baseline_values = fetch_baseline_values(
        './data/lungs/BaselinePostTransplantSurvival.json'
    )
    for baseline_value in baseline_values:
        score.append(baseline_value**exponent)
    return score


def compute_under_curb_area(values):
    res = 0
    k = 2
    i = 0

    while i < len(values):
        res += values[i] * (k - 1) * 1
        i += 1
        k += 1
    return res


def lungs_final_score(receiver, donor, receiver_listing):
    # get listing lung
    # select * from lungs where listing_id = receiver_listing.id
    # all values valid ? proceed : return error msg

    listing_lung = (
        db.session.query(Lung).filter_by(listing_id=receiver_listing.id).first()
    )

    if not listing_lung:
        raise NotFoundError("No listing found in lungs table")
    for var in dir(listing_lung):
        if var is None:
            print("Not all variables are filled, can't compute score")
            return

    Swl = next_year_survival_chance(receiver, receiver_listing, listing_lung)
    Stx = post_transplant_survival_chance(
        receiver, receiver_listing, listing_lung
    )
    # WL = sum(Swl)
    WL = compute_under_curb_area(Swl)
    PT = compute_under_curb_area(Stx)
    RawScore = decimal.Decimal(PT) - 2 * WL
    return RawScore


def normalized_lung_allocation_score(RawScore):
    LASi = (100 * (RawScore + 730)) / 1095
    return LASi


def check_NLAS(RawScore):
    if RawScore == -730 and normalized_lung_allocation_score(RawScore) == 0:
        return 0
    if RawScore == 365 and normalized_lung_allocation_score(RawScore) == 100:
        return 0
    else:
        return 1
