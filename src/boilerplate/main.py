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
    data = dat.Data()
    data()
    
    return data


if __name__ == "__main__":
    data = main()
    person = dat.Person(name="Gunnar", age=67)
    person.disp()
