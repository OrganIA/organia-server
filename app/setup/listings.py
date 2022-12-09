import random

from app import db
from app.api.listings import ListingCreateSchema, create_listing
from app.api.person import PersonCreateSchema
from app.db.models import Heart, Hospital, Lung

from . import fake


def random_bool():
    return random.choice([True, False])


def common_data():
    return {
        'start_date': fake.date(),
        'weight_kg': random.randint(40, 200) + random.randint(0, 100) / 100,
        'height_cm': random.randint(100, 200),
        'person': PersonCreateSchema(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            birth_date=fake.date(),
            abo=random.choice(['A', 'B', 'AB', 'O']),
            rhesus=random.choice(['+', '-']),
            gender=random.choice(['MALE', 'FEMALE']),
        ),
    }


def random_heart_mal():
    return random.choice(
        [
            Heart.DiagnosisGroup.VALVULAR,
            Heart.DiagnosisGroup.CONGENITAL,
            Heart.DiagnosisGroup.CONGENITAL_NON_EISENMENGER,
            *[None] * 10,
        ]
    )


def main():
    i = 0
    hospitals = db.session.query(Hospital).all()

    def random_hospital():
        return random.choice(hospitals)

    while True:
        i += 1
        type = 'DONOR' if i % 10 == 0 else 'RECEIVER'
        if i <= 30:
            organ_type = 'LIVER'
            organ = {
                "tumors_count": random.randint(0, 10),
                "biggest_tumor_size": random.randint(0, 100),
                "alpha_fetoprotein": random.randint(0, 1500),
            }
        elif i <= 60:
            organ_type = 'LUNG'
            organ = {
                "diagnosis_group": random.choice(Lung.DiagnosisGroup.values()),
                "detailed_diagnosis": random.choice(
                    Lung.DetailedDiagnosis.values()
                ),
                "body_mass_index": random.randint(150, 400) / 10,
                "diabetes": random_bool(),
                "assistance_required": random_bool(),
                "pulmonary_function_percentage": random.randint(80, 120) / 100,
                "pulmonary_artery_systolic": random.randint(200, 300),
                "oxygen_requirement": random.randint(0, 100) / 100,
                "six_minutes_walk_distance_over_150_feet": random_bool(),
                "continuous_mech_ventilation": random_bool(),
                "carbon_dioxide_partial_pressure": (
                    random.randint(300, 500) / 10
                ),
                "carbon_dioxide_partial_pressure_15_percent_increase": random_bool(),
                "activities_of_daily_life_required": random_bool(),
                "pulmonary_capilary_wedge_pressure": random.randint(0, 200)
                / 10,
                "creatinine": random.randint(0, 200) / 10,
            }
        elif i <= 90:
            organ_type = 'KIDNEY'
            dialysis = random_bool()
            retranplantation = random_bool()
            organ = {
                "is_under_dialysis": dialysis,
                "is_retransplantation": retranplantation,
                "dialysis_start_date": fake.date() if dialysis else None,
                "arf_date": fake.date(),
                "date_transplantation": (
                    fake.date() if retranplantation else None
                ),
                "re_registration_date": (
                    fake.date() if retranplantation else None
                ),
                "A": random.randint(0, 100) / 10,
                "B": random.randint(0, 100) / 10,
                "DR": random.randint(0, 100) / 10,
                "DQ": random.randint(0, 100) / 10,
            }
        elif i <= 120:
            organ_type = 'HEART'
            organ = {
                "emergency": random.choice(Heart.Emergency.values()),
                "delay_var_bio_GRF": random.randint(0, 100),
                "MAL": random_heart_mal(),
                "MAL2": random_heart_mal(),
                "MAL3": random_heart_mal(),
                "DA": random.randint(0, 10),
                "DAURG": random.randint(0, 10),
                "XPC": random.randint(0, 10),
                "BILI": random.randint(0, 100) / 10,
                "CREAT": random.randint(0, 100) / 10,
                "F_ICAR": random.randint(0, 100) / 10,
                "ICAR": random.randint(0, 100) / 10,
                "KXPC": random.randint(0, 100) / 10,
                "DIA_is_O": random_bool(),
                "DBILI": fake.date(),
                "DCREAT": fake.date(),
            }
        else:
            break
        if type == 'DONOR':
            organ = None
        create_listing(
            data=ListingCreateSchema(
                organ_type=organ_type,
                type=type,
                organ=organ,
                hospital_id=random_hospital().id,
                **common_data(),
            )
        )
