
# Table of Contents

1.  [To do](#org78bf5ec)
2.  [Description](#org7d0760d)
3.  [Input](#org3afd214)
4.  [Output](#orgadc8d96)
5.  [Usage](#orga5ab4a0)
    1.  [`uv`](#org75b3b7b)
    2.  [FastAPI](#org8561ad5)
        1.  [POST query](#org9e2ffd6)
        2.  [GET query](#org9af60dc)
        3.  [Browser](#orgd80324b)



<a id="org78bf5ec"></a>

# To do

1.  [ ] Add docstrings
2.  [ ] Add tests to pre-commit


<a id="org7d0760d"></a>

# Description


<a id="org3afd214"></a>

# Input


<a id="orgadc8d96"></a>

# Output


<a id="orga5ab4a0"></a>

# Usage


<a id="org75b3b7b"></a>

## `uv`

    uv run -m boilerplate.main


<a id="org8561ad5"></a>

## FastAPI

Launch with `uv`:

    uv run uvicorn boilerplate.api:app --reload


<a id="org9e2ffd6"></a>

### POST query

    curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
      -H "Content-Type: application/json" \
      -d '{"name":"Amine","age":44}'


<a id="org9af60dc"></a>

### GET query

[`http://127.0.0.1:8000/yob?current_year=2025&name=Amine&age=25`](http://127.0.0.1:8000/yob?current_year=2025&name=Amine&age=25)


<a id="orgd80324b"></a>

### Browser

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

