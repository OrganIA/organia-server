import pdftotext
import logging
import re

from app import db
from app.models import Hospital
from app.api.schemas.hospital import (
    HospitalSchema,
)

IS_DEPARTMENT = re.compile(r'^\d(?:\d|A|B)\d?$')


# Load your PDF
with open("./liste.pdf", "rb") as f:
    pdf = pdftotext.PDF(f)


# Read all the text into one string
# print("\n\n".join(pdf))


# How many pages?
print(len(pdf))

def store_hospital(department, city, name, hospital: HospitalSchema):
    hospital = Hospital(**hospital.dict())
    hospital.department = department
    hospital.city = city
    hospital.name = name
    db.session.add(hospital)
    db.session.commit()

def convert(string):
    li = string.split("\n")
    remove_space = li
    for index, el in enumerate(remove_space):
        try:
            if not IS_DEPARTMENT.match(el):
                continue
            department_code = el
            start_city = remove_space.index('', index) + 1
            start_hospital = remove_space.index('', start_city) + 1
            city = ' '.join(remove_space[start_city: start_hospital]).strip()
            next_department = remove_space.index('', start_hospital)
            hospital = ' '.join(remove_space[start_hospital: next_department]).strip()
            for var in [city, hospital]:
                if IS_DEPARTMENT.match(var) or var.startswith("TCA : "):
                    logging.warning("department: %s, city: %s, hospital: %s", department_code, city, hospital)
                    raise Exception
            print(department_code, city, hospital, sep='/')
            store_hospital(department_code, city, hospital)
        except Exception:
            print("Skipped")


for number, page in enumerate(pdf):
    print(number)
    convert(page)
    