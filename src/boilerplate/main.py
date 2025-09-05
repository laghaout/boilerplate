# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:44:24 2025

@author: Amine
"""

try:
    from . import schemas as dat
except Exception:
    import schemas as dat


def main():
    person = dat.Person(name="Amine", age=44)
    return person


if __name__ == "__main__":
    person = main()
    person.disp()
