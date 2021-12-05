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


def get_blood_donor(donor: Person, receiver: Person):
    if (donor.abo.value == "O"):
        return compatibility_O(receiver)
    elif (donor.abo.value == "A"):
        return compatibility_A(receiver)
    elif (donor.abo.value == "B"):
        return compatibility_B(receiver)
    elif (donor.abo.value == "AB"):
        return compatibility_AB(receiver)


def compute_scoring(donor: Person, receiver: Person, receiver_listing: Listing):
    blood_type = get_blood_donor(donor, receiver)
    organs_score = organs_priority(receiver_listing.organ)

    age = int(receiver.age)
    print("blood_type: ", blood_type)
    print("organs_score: ", organs_score)
    print("age: ", age)
    # TODO : Add conditions to check the organ and redirect to correct scoring functions
    score = organs_score * (100 + (blood_type + age)) / 3.5
    return score


@router.get('/listing/{person_id}')
async def calculate_organ(person_id: int):
    result_listing = []
    # Organ condition needed only if we decide that a donor can have multiple organs to donate
    donor = db.session.query(Listing).filter((Listing.person_id==person_id)).first()
    if (donor is None):
        return "No listing found for this person_id with this organ"
    receivers = db.session.query(Listing).filter_by(donor=False).all()
    for receiver in receivers:
        score = compute_scoring(donor.person, receiver.person, receiver)
        result_listing.append({"listing": receiver, "score": score})
    return sorted(result_listing, key=lambda x: x["score"], reverse=True)