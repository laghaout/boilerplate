# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 21:37:41 2025

@author: amine
"""

# src/boilerplate/api.py
from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, Field

# Support both "module" and "script/IDE" execution contexts
try:
    from . import schemas as dat  # uv run -m / uvicorn boilerplate.api:app
except Exception:
    import schemas as dat  # running file directly in an IDE

app = FastAPI(title="Boilerplate API", version="0.1.0")


class YobResponse(BaseModel):
    year_of_birth: int = Field(..., description="Computed year of birth")


@app.post("/yob", response_model=YobResponse)
def yob_from_person(
    person: dat.Person,
    current_year: int = Query(..., ge=0, description="Calendar year to compute from"),
):
    try:
        return YobResponse(year_of_birth=person.yob(current_year))
    except Exception as e:
        # Keep behavior clear if the model method raises
        raise HTTPException(status_code=500, detail=f"Person.yob() failed: {e}")


@app.get("/yob", response_model=YobResponse)
def yob_from_query(
    name: str,
    age: int = Query(..., ge=0, description="Age in full years"),
    current_year: int = Query(..., ge=0, description="Calendar year to compute from"),
):
    try:
        p = dat.Person(name=name, age=age)
        return YobResponse(year_of_birth=p.yob(current_year))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Person.yob() failed: {e}")


"""
uv run uvicorn boilerplate.api:app --reload


curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
  -H "Content-Type: application/json" \
  -d '{"name":"Amine","age":44}'


http://127.0.0.1:8000/docs
"""
