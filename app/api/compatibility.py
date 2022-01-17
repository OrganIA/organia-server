from app.models import Person


def compatibility_positive(receiver: Person):
    return {
        "O+": 9,
        "O-": 9,
        "AB+": 10,
        "AB-": 10,
        "A+": 9,
        "A-": 9,
        "B+": 10,
        "B-": 10,
    }.get(receiver.blood_type, 1)


def compatibility_negative(receiver: Person):
    return {
        "O+": 5,
        "AB+": 9,
        "A+": 5,
        "B+": 8,
    }.get(receiver.blood_type, 1)


def compatibility_score(receiver: Person):
    if (receiver.rhesus == Person.Rhesus.NEGATIVE):
        return compatibility_negative(Person)
    else:
        return compatibility_positive(Person)
