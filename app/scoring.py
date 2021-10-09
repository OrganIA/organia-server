def heart_scoring(age, rhesus, blood_type_receveir, blood_type_donor):
    
    blood_type = compatibility(blood_type_donor)
    if rhesus == '-':
        rhesus = -1
    else:
        rhesus = 1
    score = 100 * (rhesus + blood_type + age) / 3
    return score

def compatibility(blood_type_donor):
    if blood_type_donor == "A":
        blood_type = 1
    elif blood_type_donor == "B":
        blood_type = 2
    elif blood_type_donor == "AB":
        blood_type = 3
    else:
        blood_type = 4
    return blood_type