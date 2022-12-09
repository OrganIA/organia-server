import logging

from faker import Faker

from app import config, db
from app.db.models import User

ENVIRONMENT_WHITELIST = ['dev', 'demo']

fake = Faker("fr_FR")

from . import hospitals, listings, users


def main():
    if (
        config.ENVIRONMENT not in ENVIRONMENT_WHITELIST
        and not config.LOAD_FAKE_DATA
    ) or db.session.query(User).count() > 0:
        logging.debug('Skipping fake data setup')
        return
    logging.info('Starting the fake data setup')
    users.main()
    hospitals.main()
    listings.main()
    db.session.commit()


def setup_hospitals():
    import csv

    with open("./data/hospitals.csv", encoding='latin1') as f:
        data = list(csv.reader(f, delimiter=';'))
    done = 0
    for line in data:
        if done == 0:
            done += 1
            continue
        hospital = {
            'name': line[4],
            'city': line[15][line[15].find(' ') + 1 :],
        }
        logging.info(hospital)
