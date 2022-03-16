import json


def fetch_baseline_values():
    with open('./BaselineWaitingListSurvival.json', 'r') as f:
        data = json.load(f)
    return data["data"]


def calculate_exponent(receiver, receiver_listing):
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
    return e


def next_year_survival_chance(receiver, receiver_listing):
    score = []

    exponent = calculate_exponent(receiver, receiver_listing)
    baseline_values = fetch_baseline_values()
    for baseline_value in baseline_values:
        score.append(baseline_value ** exponent)
    return score


def lungs_final_score(receiver, donor, receiver_listing):
    next_year_survival_chance(receiver, receiver_listing)
    return 42
