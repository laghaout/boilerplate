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
    persons = dat.Persons()
    persons()    
    return persons.persons


@app.post("/age", response_model=dat.Output_age)
def get_age_POST(
    person: dat.Person,
    current_year: int = Query(
        ..., ge=0, description="Calendar year to compute from"),
):
    try:
        age = person.get_age(current_year)
        return dat.Output_age(age=age)
    except Exception as e:
        # Keep behavior clear if the model method raises
        raise HTTPException(
            status_code=500, detail=f"Person.get_age() failed: {e}")


@app.get("/age", response_model=dat.Output_age)
def get_age_GET(
    name: str,
    yob: int = Query(..., ge=0, description="Year of birth"),
    current_year: int = Query(
        ..., ge=0, description="Calendar year to compute from"),
):
    try:
        person = dat.Person(name=name, yob=yob)
        age = person.get_age(current_year)
        return dat.Output_age(age=age)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Person.get_age() failed: {e}")    