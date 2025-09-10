# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:45:42 2025

@author: amine
"""

from pydantic import BaseModel, Field
from typing import Optional


class YobOutput(BaseModel):
    year_of_birth: int = Field(..., description="Computed year of birth")


class Person(BaseModel):
    name: str
    age: int
    attributes: Optional[list] = []

    def disp(self):
        print(f"{self.name} is {self.age} years old.")

    def yob(self, current_year: int) -> int:
        year_of_birth = current_year - self.age
        print(f"{self.name}'s year of birth is {year_of_birth}.")
        return year_of_birth
    
    def add_attribute(self, attribute: object):
        self.attributes.append(attribute)

    def get_attribute_at(self, position: int):
        return self.attributes[position]