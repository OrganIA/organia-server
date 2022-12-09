import logging
import re
import sys

import pdftotext

from app import db
from app.db.models import City, Hospital

IS_DEPARTMENT = re.compile(r'^\d(?:\d|A|B)\d?$')


def store_hospital(department, city, name):
    if not (city_obj := db.session.query(City).filter_by(name=city).first()):
        city_obj = City(name=city, department_code=department)
        db.session.add(city_obj)
    hospital = Hospital(name=name, city=city_obj)
    db.session.add(hospital)


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
            city = ' '.join(remove_space[start_city:start_hospital]).strip()
            next_department = remove_space.index('', start_hospital)
            hospital = ' '.join(
                remove_space[start_hospital:next_department]
            ).strip()
            for var in [city, hospital]:
                if IS_DEPARTMENT.match(var) or var.startswith("TCA : "):
                    logging.debug(
                        "department: %s, city: %s, hospital: %s",
                        department_code,
                        city,
                        hospital,
                    )
                    raise Exception
            store_hospital(department_code, city, hospital)
        except Exception:
            logging.debug("Skipped")


def main():
    with open("./data/hospitals_list.pdf", "rb") as f:
        pdf = pdftotext.PDF(f)
    for number, page in enumerate(pdf):
        logging.debug("Page: %d", number)
        convert(page)
