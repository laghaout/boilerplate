# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:44:24 2025

@author: amine
"""

try:
    from . import schemas as dat
except Exception:
    import schemas as dat

    
def main() -> dict:
    persons = dat.Persons()
    persons()
    
    return persons


if __name__ == "__main__":
    persons = main()
    person = dat.Person(name="Olof", age=67)
    person.disp()
