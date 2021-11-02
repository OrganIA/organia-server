#THE VALUE WILL BE CHANGE LATER

def compatibility_O(donor_blood, receiver_blood, rhesus_donor, rhesus_receiver):
    print("DONNEUR",donor_blood, receiver_blood, rhesus_donor, rhesus_receiver)
    blood_score = 1
    if (rhesus_receiver == '-'):
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

def compatibility_A(donor_blood, receiver_blood, rhesus_donor, rhesus_receiver):
    print("DONNEUR",donor_blood, receiver_blood, rhesus_donor, rhesus_receiver)
    blood_score = 1
    if (rhesus_receiver == '-'):
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

def compatibility_B(donor_blood, receiver_blood, rhesus_donor, rhesus_receiver):
    print("DONNEUR",donor_blood, receiver_blood, rhesus_donor, rhesus_receiver)
    blood_score = 1
    if (rhesus_receiver == '-'):
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

def compatibility_AB(donor_blood, receiver_blood, rhesus_donor, rhesus_receiver):
    print("DONNEUR",donor_blood, receiver_blood, rhesus_donor, rhesus_receiver)
    blood_score = 1
    if (rhesus_receiver == '-'):
        if (receiver_blood == 'AB+'):
            blood_score = 10
        if (receiver_blood == 'AB-'):
            blood_score = 10
    else:
        if (receiver_blood == 'AB+'):
            blood_score = 9
    return blood_score