# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:44:24 2025

@author: amine
"""

from pathlib import Path

try:
    from . import schemas as dat
except Exception:
    import schemas as dat


ROOT = Path(__file__).resolve().parent.parents[1]

def main() -> dict:
    data = dat.Data(
        # root_dir=ROOT.parts,
        # config=["config", "config.json"],
        )
    data()
    
    return data


if __name__ == "__main__":
    data = main()
    person = dat.Person(name="Gunnar", age=67)
    person.disp()
