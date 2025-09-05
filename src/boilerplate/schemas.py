# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:45:42 2025

@author: Amine
"""

from pydantic import BaseModel


class Person(BaseModel):
    name: str
    age: int

    def disp(self):
        print(f"{self.name} is {self.age} years old.")

    def yob(self, current_year: int):
        print(f"{self.name}'s year of birth is {current_year - self.age}.")
