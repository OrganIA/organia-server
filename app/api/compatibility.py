from app.models import Person

def compatibility_O(receiver: Person):
    blood_score = 1
    if (receiver.rhesus == '-'):
        if (receiver.blood_type == 'O+'):
            blood_score = 9
        if (receiver.blood_type == 'O-'):
            blood_score = 9
        if (receiver.blood_type == 'AB+'):
            blood_score = 10
        if (receiver.blood_type == 'AB-'):
            blood_score = 10
        if (receiver.blood_type == 'A+'):
            blood_score = 9
        if (receiver.blood_type == 'A-'):
            blood_score = 9
        if (receiver.blood_type == 'B+'):
            blood_score = 10
        if (receiver.blood_type == 'B-'):
            blood_score = 10
    else:
        if (receiver.blood_type == 'O+'):
            blood_score = 5
        if (receiver.blood_type == 'AB+'):
            blood_score = 9
        if (receiver.blood_type == 'A+'):
            blood_score = 5
        if (receiver.blood_type == 'B+'):
            blood_score = 8
    return blood_score


def compatibility_A(receiver: Person):
    blood_score = 1
    if (receiver.rhesus == '-'):
        if (receiver.blood_type == 'AB+'):
            blood_score = 10
        if (receiver.blood_type == 'AB-'):
            blood_score = 10

        if (receiver.blood_type == 'A+'):
            blood_score = 9
        if (receiver.blood_type == 'A-'):
            blood_score = 9
    else:
        if (receiver.blood_type == 'AB+'):
            blood_score = 5
        if (receiver.blood_type == 'A+'):
            blood_score = 5
    return blood_score


def compatibility_B(receiver: Person):
    blood_score = 1
    if (receiver.rhesus == '-'):
        if (receiver.blood_type == 'AB+'):
            blood_score = 10
        if (receiver.blood_type == 'AB-'):
            blood_score = 10
        if (receiver.blood_type == 'B+'):
            blood_score = 10
        if (receiver.blood_type == 'B-'):
            blood_score = 10
    else:
        if (receiver.blood_type == 'AB+'):
            blood_score = 9
        if (receiver.blood_type == 'B+'):
            blood_score = 8
    return blood_score


def compatibility_AB(receiver: Person):
    blood_score = 1
    if (receiver.rhesus == '-'):
        if (receiver.blood_type == 'AB+'):
            blood_score = 10
        if (receiver.blood_type == 'AB-'):
            blood_score = 10
    else:
        if (receiver.blood_type == 'AB+'):
            blood_score = 9
    return blood_score
