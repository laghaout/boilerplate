# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:44:24 2025

@author: amine
"""

try:
    from . import schemas as dat
    from . import utilities as util
except Exception:
    import schemas as dat
    import utilities as util


def main() -> dict:
    persons = dat.Persons()  # Initialize
    persons()  # ETL
    persons.engineer()  # Engineer the feature vectors
    # persons.explore()  # Explore the data
    persons.save()  # Save to disk

    # Create some random person.
    person = dat.Person(name="Olof", yob=1958)
    person.disp()

    return persons


if __name__ == "__main__":
    
    try:
        reloaded = dat.Persons.load()
        persons = reloaded.pop("persons_pkl")
    except Exception:
        persons = main()
    util.close_loggers()
