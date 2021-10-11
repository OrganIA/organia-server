from typing import List
from fastapi import APIRouter

from datetime import datetime
from app import db
from app.errors import NotFoundError
from app.models import Person
from app.models import Listing
from app import scoring
from app.api.schemas.person import (
    PersonSchema, PersonGetSchema, PersonUpdateSchema,
)
from .dependencies import logged_user


router = APIRouter(prefix='/score') # D²o not forget to add permissions


@router.get('/{listing_id}')
async def get_receivers_from_donor():
    return db.session.query(Person).all()


def compatibility(donor_blood, receiver_blood, rhesus_donor):
    if rhesus_donor == '+':
        if donor_blood == 'O':
            blood_score = 4
        elif donor_blood == 'A' and receiver_blood == 'A':
            blood_score = 5
        elif donor_blood == 'B' and receiver_blood == 'AB':
            blood_score = 3
        elif donor_blood == 'AB' and receiver_blood == 'O':
            blood_score = 2
        else:
            blood_score = 1
    else:
        if donor_blood == 'O':
            blood_score = 2
        elif donor_blood == 'A' and receiver_blood == 'A':
            blood_score = 2
        elif donor_blood == 'B' and receiver_blood == 'B':
            blood_score = 1
        elif donor_blood == 'AB' and receiver_blood == 'AB':
            blood_score = 1
        else:
            blood_score = 1
    return blood_score    

def organs_priority(organs):
    if organs == "HEART":
        organs_score = 1
    elif organs == "KIDNEYS":
        organs_score = 2
    else:
        organs_score = 3
    return organs_score

def compute_scoring(donor: Listing, receiver: Listing):
    blood_type = compatibility(donor.person.blood_type, receiver.person.blood_type, donor.person.rhesus)
    organs_score = organs_priority(receiver.organ)

    age = int(donor.person.age)
    score = 100 * (blood_type * (organs_score +  age)) / 3.5
    return score


@router.get('/listing/{person_id}')
async def calculate_heart(person_id: int):
    heart_listing = []
    donor = db.session.query(Listing).filter(Listing.person_id==person_id).first()
    receivers = db.session.query(Listing).filter_by(organ=donor.organ, donor=False).all()
    for receiver in receivers:
        score = compute_scoring(donor, receiver)
        heart_listing.append({"listing": receiver, "score": score}) # Placeholder value until branches are merged
    return (heart_listing)
