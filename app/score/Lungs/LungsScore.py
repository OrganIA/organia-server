from http.client import NON_AUTHORITATIVE_INFORMATION
import json


def fetch_baseline_values(file):
    with open(file, 'r') as f:
        data = json.load(f)
    return data["data"]


def calculate_next_year_survival_chance_exponent(receiver, receiver_listing):
    e = 0

    if (receiver_listing.diagnosis_group == "A" or receiver_listing.diagnosis_group == "B"
            or receiver_listing.diagnosis_group == "C"):
        e += receiver.age * 0.015097  # Age Today - Birthday
    elif (receiver_listing.diagnosis_group == "D"):
        e += receiver.age * 0.021223  # Age
    e += receiver_listing.body_mass_index * (-0.051781)  # Body Mass
    if (receiver_listing.diabetes):
        e += 0.158821
    if (receiver_listing.functional_status_assistance_required):
        e += 0.115024
    else:
        e += 0.182250
    e += receiver_listing.FVC_percentage * (-0.019675)  # FVC not sure about %
    if (receiver_listing.diagnosis_group == "A" or receiver_listing.diagnosis_group == "D"
            or receiver_listing.diagnosis_group == "C"):
        e += receiver_listing.PA_systolic * 0.015889  # PA
    if (receiver_listing.diagnosis_group == "A" or receiver_listing.diagnosis_group == "D"):
        e += receiver_listing.oxygen_requirement * 0.187599  # 02 requirement at rest
    elif (receiver_listing.diagnosis_group == "B"):
        e += receiver_listing.oxygen_requirement * 0.040766  # 02 requirement at rest
    elif (receiver_listing.diagnosis_group == "C"):
        e += receiver_listing.oxygen_requirement * 0.125568  # 02 requirement at rest
    if (receiver_listing.six_minute_walk_distance_over_150_feet):
        e += 0.330752
    if (receiver_listing.continuous_mechanical_ventilation):
        e += 1.213804
    e += (receiver_listing.PCO2 - 40) * 0.005448  # PCO2
    if (receiver_listing.PCO2_increase_superior_to_15_percent):
        e += 0.076370
    if (receiver_listing.diagnosis_group == "B"):
        e += 2.376700
    elif (receiver_listing.diagnosis_group == "C"):
        e += 0.943377
    elif (receiver_listing.diagnosis_group == "D"):
        e += 0.996936
    if receiver_listing.detailled_diagnosis == "Bronchiectasis":
        e += 0.157212
    elif receiver_listing.detailled_diagnosis == "Eisenmenger":
        e += -0.627866
    elif receiver_listing.detailled_diagnosis == "Lymphangioleiomyomatosis":
        e += -0.197434
    elif receiver_listing.detailled_diagnosis == "Bronchiolitis":
        e += -0.256480
    elif receiver_listing.detailled_diagnosis == "Bronchiolitis":
        e += -0.265233
    if receiver_listing.detailled_diagnosis == "Sarcoidosis" and receiver_listing.PA_systolic > 30:
        e += -0.707346
    elif receiver_listing.detailled_diagnosis == "Sarcoidosis" and receiver_listing.PA_systolic <= 30:
        e += 0.455348
    return e


def next_year_survival_chance(receiver, receiver_listing):
    score = []

    exponent = calculate_next_year_survival_chance_exponent(
        receiver, receiver_listing)
    baseline_values = fetch_baseline_values(
        './data/BaselineWaitingListSurvival.json')
    for baseline_value in baseline_values:
        score.append(baseline_value ** exponent)
    return score


def calculate_post_transplant_survival_chance_exponent(receiver, receiver_listing):
    e = 0

    if receiver_listing.diagnosis_group == 'B':
        e += 0.623207
        e += receiver_listing.FVC_percentage
    elif receiver_listing.diagnosis_group == 'C':
        e += 0.008514
    elif receiver_listing.diagnosis_group == 'D':
        e += 0.413173
        e += receiver_listing.FVC_percentage
        if receiver_listing.PCW_over_20_mmHg:
            e += 0.033046

    e += receiver_listing.age_at_transplant * 0.003510
    e += receiver_listing.creatinine_at_transplant * 0.061986
    if receiver_listing.ADL_required:
        e += -0.488525
    if receiver_listing.continuous_mechanical_ventilation:
        e += 0.312846

    if (receiver_listing.detailled_diagnosis == "Bronchiectasis"):
        e += 0.056116
    elif (receiver_listing.detailled_diagnosis == "Eisenmenger"):
        e += 0.393526
    elif (receiver_listing.detailled_diagnosis == "Lymphangioleiomyomatosis"):
        e += -0.624209
    elif (receiver_listing.detailled_diagnosis == "Bronchiolitis"):
        e += -0.443786
    if receiver_listing.detailled_diagnosis == "Sarcoidosis" and receiver_listing.PA_systolic > 30:
        e += -0.122351
    elif receiver_listing.detailled_diagnosis == "Sarcoidosis" and receiver_listing.PA_systolic <= 30:
        e += -0.016505

    return e


def post_transplant_survival_chance(receiver, receiver_listing):
    score = []

    exponent = calculate_post_transplant_survival_chance_exponent(
        receiver, receiver_listing)
    baseline_values = fetch_baseline_values(
        '.data\BaselinePostTransplantSurvival.json')
    for baseline_value in baseline_values:
        score.append(baseline_value ** exponent)
    return score


def compute_under_curb_area(values):
    res = 0
    k = 2
    i = 0

    while (i < len(values)):
        res += values[i] * (k - 1) * 1
        i += 1
        k += 1
    return res


def lungs_final_score(receiver, donor, receiver_listing):
    Swl = next_year_survival_chance(receiver, receiver_listing)
    Stx = post_transplant_survival_chance(receiver, receiver_listing)
    # WL = sum(Swl)
    WL = compute_under_curb_area(Swl)
    PT = compute_under_curb_area(Stx)
    RawScore = PT - 2 * WL
    return 42


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
