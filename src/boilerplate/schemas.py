# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:45:42 2025

@author: amine
"""

from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int

    def disp(self):
        print(f"{self.name} is {self.age} years old.")

    def yob(self, current_year: int) -> int:
        year_of_birth = current_year - self.age
        print(f"{self.name}'s year of birth is {year_of_birth}.")
        return year_of_birth
