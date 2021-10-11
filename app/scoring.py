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

def organs_priority(organs):
    if organs == HEART:
        organs_score = 1
    elif organs == KIDNEYS:
        organs_score = 2
    else:
        organs_score = 3
    return organs_score

def heart_scoring(age, rhesus, organs, blood_type_donor):
    blood_type = compatibility(blood_type_donor)
    organs_score = organs_priority(organs)
    if rhesus == '-':
        rhesus = -1
    else:
        rhesus = 1
        
    score = 100 * (rhesus + age + (organs_score +  blood_type)) / 3
    return score