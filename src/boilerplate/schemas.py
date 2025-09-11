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
from typing import Any, Dict, List, Optional

try:
    from . import utilities as util
except Exception:
    import utilities as util

class Person(BaseModel):
    name: str
    yob: int
    attributes: List[str] = None
    age: Optional[int] = None

    def disp(self):
        util.disp(f"{self.name} was born in {self.yob}.")

    def get_age(self, current_year: int) -> int:
        age = current_year - self.yob
        util.disp(f"{self.name} is {age} years old.")
        return age
    
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
        self.config.data = self.root_dir / Path(*self.config.data)
        self.config.output = self.root_dir / Path(*self.config.output)
        
    def __call__(self):
        import pandas as pd
        df = pd.read_csv(self.config.data)
        df["attributes"] = df["attributes"].apply(ast.literal_eval)
        records = df.to_dict(orient="records")
        adapter = TypeAdapter(List[Person])
        self.persons = {
            k: v for k, v in enumerate(adapter.validate_python(records))}

    def save_persons(self, directory: list=None, filename: str="persons.json"):
        if directory is None:
            directory = self.config.output
        else:
            directory = Path(*directory)
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / Path(*[filename])
        
        persons: Dict[str, Person] = {
            str(k): v for k, v in (self.persons or {}).items()
        }
    
        persons = TypeAdapter(Dict[str, Person]).dump_json(persons, indent=2)
        path.write_bytes(persons)
        
    @staticmethod
    def load_persons(directory: list | None = None, filename: str = "persons.json") -> Dict[str, Person]:
   
        path = Path(*directory) / Path(*[filename])
        if not path.exists():
            raise FileNotFoundError(f"No saved persons file found at {path}")
    
        data = path.read_bytes()
        persons = TypeAdapter(Dict[str, Person]).validate_json(data)
    
        return persons        
        
#%% FastAPI wrappers
    
class Output_age(BaseModel):
    age: int = Field(..., description="Computed age")    