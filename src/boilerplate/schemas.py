# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 19:45:42 2025

@author: amine
"""

import ast
import json
import numpy as np
import pandas as pd
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
    attributes: Optional[List[str]] = None
    age: Optional[int] = None
    embedding: Optional[List[float]] = None

    def set_embedding(self):
        self.embedding = np.random.rand(10).tolist()

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
    data: object = None
    root_dir: Path | List[str]=Path(__file__).resolve().parent.parents[1]
    config: dict | List[str] = ["config", "config.json"]

    def model_post_init(self, __context: Dict[str, Any]) -> None:
        # Specify the root directory.
        if isinstance(self.root_dir, list):
            self.root_dir = Path(*self.root_dir)
            
        # Load the configuration parameters.
        if isinstance(self.config, list):
            self.config = self.root_dir / Path(*self.config)
            with open(self.config) as file:
                self.config = json.load(file)
        self.config = SimpleNamespace(**self.config)
        
        # Construct the path to the data and output directories.
        self.config.data = self.root_dir / Path(*self.config.data)
        self.config.output = self.root_dir / Path(*self.config.output)
        
    def __call__(self):
        """ 
        Extract-Transform-Load into a dictionary of Pydantic objects. This is 
        also where the data validation happens.
        """
        persons = pd.read_csv(self.config.data)
        # Person attributes are lists, so make sure they're read as such.
        persons["attributes"] = persons["attributes"].apply(ast.literal_eval)
        records = persons.to_dict(orient="records")
        adapter = TypeAdapter(List[Person])
        
        self.persons = {
            persons.index[k]: v 
            for k, v in enumerate(adapter.validate_python(records))}
        
    def engineer(self) -> pd.DataFrame:
        
        # Embed all the Person objects
        [person.set_embedding() for person in self.persons.values()]
        
        self.data = pd.DataFrame.from_dict(
            {k: v.model_dump() for k, v in self.persons.items()}, 
            orient="index"
        )
        
    def explore(self, data: pd.DataFrame=None):
        if data is None:
            data = self.data
        
        data["embedding"] = data["embedding"].map(np.array)
        util.project_dataframe_in_tensorboard(
            data, "embedding", self.config.output)

    def save(self, directory: Path | list=None):
        """ Save `self.persons` """
        # Use the configured output directory unless otherwise specified.
        if directory is None:
            directory = self.config.output
        elif isinstance(directory, list):
            directory = Path(*directory)
        directory.mkdir(parents=True, exist_ok=True)
        
        # Save the `persons`.
        path = directory / Path(*["persons.json"])
        persons: Dict[str, Person] = {
            str(k): v for k, v in (self.persons or {}).items()
        }
        persons = TypeAdapter(Dict[str, Person]).dump_json(persons, indent=2)
        path.write_bytes(persons)
        
        # Save the `data`.
        path = directory / Path(*["data.csv"])        
        self.data.to_csv(path, index=True)
        
    @staticmethod
    def load(directory: Path | list = Path(__file__).resolve().parent.parents[1] / Path(*["output"])) -> dict:
        if isinstance(directory, list):
            directory = Path(*directory)
    
        # Load the `persons`
        path = directory / Path(*["persons.json"])
        if not path.exists():
            raise FileNotFoundError(f"No saved persons file found at {path}")        
        persons = path.read_bytes()
        persons = TypeAdapter(Dict[str, Person]).validate_json(persons)
        
        # Load the `data`.
        path = directory / Path(*["data.csv"])
        if not path.exists():
            raise FileNotFoundError(f"No saved persons file found at {path}")
        data = pd.read_csv(path, index_col=0)
    
        return dict(
            persons=persons, 
            data=data,
            )
        
#%% FastAPI wrappers
    
class Output_age(BaseModel):
    age: int = Field(..., description="Computed age")    