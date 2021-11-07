from typing import List
from fastapi import APIRouter

from datetime import datetime
from app import db
from app.errors import NotFoundError
from app.models import Person
from app.models import Listing
from app.api.compatibility import (
    compatibility_O,
    compatibility_A,
    compatibility_B,
    compatibility_AB
)
from app.api.schemas.person import (
    PersonSchema, PersonGetSchema, PersonUpdateSchema,
)
from .dependencies import logged_user


router = APIRouter(prefix='/score') # Do not forget to add permissions


def organs_priority(organs):
    if organs == "HEART":
        organs_score = 1
    elif organs == "KIDNEYS":
        organs_score = 2
    else:
        organs_score = 3
    return organs_score


def get_blood_donor(donor: Listing, receiver: Listing):
    if (donor.person.abo.value == "O"):
        return compatibility_O(receiver.person.blood_type, receiver.person.rhesus)
    elif (donor.person.abo.value == "A"):
        return compatibility_A(receiver.person.blood_type, receiver.person.rhesus)
    elif (donor.person.abo.value == "B"):
        return compatibility_B(receiver.person.blood_type, receiver.person.rhesus)
    elif (donor.person.abo.value == "AB"):
        return compatibility_AB(receiver.person.blood_type, receiver.person.rhesus)


def compute_scoring(donor: Listing, receiver: Listing):
    blood_type = get_blood_donor(donor, receiver)
    organs_score = organs_priority(receiver.organ)

    age = int(receiver.person.age)
    # TODO : Add conditions to check the organ and redirect to correct scoring functions
    score = organs_score * (100 + (blood_type + age)) / 3.5
    return score




def calculate_heart(person_id: int):
    heart_listing = []
    donor = db.session.query(Listing).filter(Listing.person_id==person_id).first()
    if (donor is None):
        return "No listing found for this person id"
    receivers = db.session.query(Listing).filter_by(donor=False).all()
    for receiver in receivers:
        score = compute_scoring(donor, receiver)
        heart_listing.append({"listing": receiver, "score": score})
    return (sorted(heart_listing, key=lambda x: x["score"], reverse=True))


@router.get('/listing/{person_id}/{organ}')
async def calculate_organ(person_id: int, organ: str):
    result_listing = []
    # Organ condition needed only if we decide that a donor can have multiple organs to donate
    donor = db.session.query(Listing).filter((Listing.person_id==person_id) & (Listing.organ==organ)).first()
    if (donor is None):
        return "No listing found for this person_id with this organ"
    receivers = db.session.query(Listing).filter_by(donor=False).all()
    for receiver in receivers:
        score = compute_scoring(donor, receiver)
        result_listing.append({"listing": receiver, "score": score})
    return sorted(result_listing, key=lambda x: x["score"], reverse=True)