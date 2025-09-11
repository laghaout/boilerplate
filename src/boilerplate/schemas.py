# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:45:42 2025

@author: amine
"""

import ast
import json
from pathlib import Path
from pydantic import BaseModel, Field, TypeAdapter
from types import SimpleNamespace
from typing import Any, Dict, List

class Person(BaseModel):
    name: str
    age: int
    attributes: List[str] = None

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


class Persons(BaseModel):
    persons: Dict[int | str, Person] = None
    root_dir: object | List[str] = Path(__file__).resolve().parent.parents[1]
    config: dict | List[str] = ["config", "config.json"]

    def model_post_init(self, __context: Dict[str, Any]) -> None:
        if isinstance(self.root_dir, list):
            self.root_dir = Path(*self.root_dir)
        
        if isinstance(self.config, list):
            self.config = self.root_dir / Path(*self.config)
            with open(self.config) as file:
                self.config = json.load(file)
                
        self.config = SimpleNamespace(**self.config)
        self.config.data = Path(*self.config.data)
        
        
    def __call__(self):
        import pandas as pd
        df = pd.read_csv(self.root_dir / self.config.data)
        df["attributes"] = df["attributes"].apply(ast.literal_eval)
        records = df.to_dict(orient="records")
        adapter = TypeAdapter(List[Person])
        self.persons = {
            k: v for k, v in enumerate(adapter.validate_python(records))}



#%% FastAPI wrappers
    
class YobOutput(BaseModel):
    year_of_birth: int = Field(..., description="Computed year of birth")    