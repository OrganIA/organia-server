# THE VALUE WILL BE CHANGE LATER

def compatibility_O(receiver_blood, rhesus_receiver):
    blood_score = 1
    if (rhesus_receiver.value == '-'):
        if (receiver_blood == 'O+'):
            blood_score = 9
        if (receiver_blood == 'O-'):
            blood_score = 9
        if (receiver_blood == 'AB+'):
            blood_score = 10
        if (receiver_blood == 'AB-'):
            blood_score = 10
        if (receiver_blood == 'A+'):
            blood_score = 9
        if (receiver_blood == 'A-'):
            blood_score = 9
        if (receiver_blood == 'B+'):
            blood_score = 10
        if (receiver_blood == 'B-'):
            blood_score = 10
    else:
        if (receiver_blood == 'O+'):
            blood_score = 5
        if (receiver_blood == 'AB+'):
            blood_score = 9
        if (receiver_blood == 'A+'):
            blood_score = 5
        if (receiver_blood == 'B+'):
            blood_score = 8
    return blood_score


def compatibility_A(receiver_blood, rhesus_receiver):
    blood_score = 1
    if (rhesus_receiver.value == '-'):
        if (receiver_blood == 'AB+'):
            blood_score = 10
        if (receiver_blood == 'AB-'):
            blood_score = 10

        if (receiver_blood == 'A+'):
            blood_score = 9
        if (receiver_blood == 'A-'):
            blood_score = 9
    else:
        if (receiver_blood == 'AB+'):
            blood_score = 5
        if (receiver_blood == 'A+'):
            blood_score = 5
    return blood_score


def compatibility_B(receiver_blood, rhesus_receiver):
    blood_score = 1
    if (rhesus_receiver.value == '-'):
        if (receiver_blood == 'AB+'):
            blood_score = 10
        if (receiver_blood == 'AB-'):
            blood_score = 10
        if (receiver_blood == 'B+'):
            blood_score = 10
        if (receiver_blood == 'B-'):
            blood_score = 10
    else:
        if (receiver_blood == 'AB+'):
            blood_score = 9
        if (receiver_blood == 'B+'):
            blood_score = 8
    return blood_score


def compatibility_AB(receiver_blood, rhesus_receiver):
    blood_score = 1
    if (rhesus_receiver.value == '-'):
        if (receiver_blood == 'AB+'):
            blood_score = 10
        if (receiver_blood == 'AB-'):
            blood_score = 10
    else:
        if (receiver_blood == 'AB+'):
            blood_score = 9
    return blood_score
