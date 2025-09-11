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
    persons = dat.Persons()
    persons()
    
    return persons


if __name__ == "__main__":
    persons = main()
    person = dat.Person(name="Olof", yob=1958)
    person.disp()
    util.disp("Hello world!")
