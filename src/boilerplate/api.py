# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 21:37:41 2025

@author: amine
"""

from fastapi import FastAPI, Query, HTTPException


# Support both "module" and "script/IDE" execution contexts
try:
    from . import schemas as dat  # uv run -m / uvicorn boilerplate.api:app
except Exception:
    import schemas as dat  # running file directly in an IDE

app = FastAPI(title="Boilerplate API", version="0.1.0")


@app.get("/")
def root():
    return dict(some_key="some_value")


@app.post("/yob", response_model=dat.YobOutput)
def yob(
    person: dat.Person,
    current_year: int = Query(
        ..., ge=0, description="Calendar year to compute from"),
):
    try:
        year_of_birth = person.yob(current_year)
        return dat.YobOutput(year_of_birth=year_of_birth)
    except Exception as e:
        # Keep behavior clear if the model method raises
        raise HTTPException(
            status_code=500, detail=f"Person.yob() failed: {e}")


@app.get("/yob", response_model=dat.YobOutput)
def yob(
    name: str,
    age: int = Query(..., ge=0, description="Age in full years"),
    current_year: int = Query(
        ..., ge=0, description="Calendar year to compute from"),
):
    try:
        person = dat.Person(name=name, age=age)
        year_of_birth = person.yob(current_year)
        return dat.YobOutput(year_of_birth=year_of_birth)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Person.yob() failed: {e}")

@app.post("/add_attribute")
def add_attribute(person: dat.Person, attribute: object):
    person.add_attribute(attribute)
    return person.attributes

@app.get("/get_attribute_at")
def get_attribute_at(person: dat.Person, position: int):
    return person.get_attribute_at(position)
    
    