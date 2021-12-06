from typing import List
from fastapi import APIRouter

from datetime import datetime
from app import db
from app.errors import NotFoundError
from app.models import Person
from app.models import Listing
from app.api.compatibility import (
    compatibility_score,
)
from app.api.schemas.person import (
    PersonSchema, PersonGetSchema, PersonUpdateSchema,
)
from .dependencies import logged_user


router = APIRouter(prefix='/score', dependencies=[logged_user])


def organs_priority(organs):
    return {
        "HEART": 1,
        "KIDNEYS": 2,
    }.get(organs, 3)


def compute_scoring(donor: Person, receiver: Person, receiver_listing: Listing):
    blood_type = compatibility_score(receiver)
    organs_score = organs_priority(receiver_listing.organ)

    age = receiver.age
    score = organs_score * (100 + (blood_type + age)) / 3.5
    return score


@router.get('/listing/{person_id}')
async def calculate_organ(person_id: int):
    result_listing = []
    donor = db.session.query(Listing)\
        .filter((Listing.person_id == person_id)).first()
    if (donor is None):
        NotFoundError.r('Donor is not found')
    receivers = db.session.query(Listing)\
        .filter_by(donor=False).all()
    if (receivers is None):
        NotFoundError.r('List of receiver is not found')
    for receiver in receivers:
        score = compute_scoring(donor.person, receiver.person, receiver)
        result_listing.append({"listing": receiver, "score": score})
    # return sorted(result_listing, key=lambda x: x["score"], reverse=True)
    return donor.person
