
# Table of Contents

1.  [To do](#orgd9b7d4a)
2.  [Description](#orgd17c0df)
3.  [Input](#org798f791)
4.  [Output](#org3964172)
5.  [Usage](#org53d5c42)
    1.  [`uv`](#org2f8d5f5)
    2.  [FastAPI](#orga55d1a2)
        1.  [POST query](#org7e5ce88)
        2.  [Get query](#org3e9a511)
        3.  [Browser](#org5971a3e)



<a id="orgd9b7d4a"></a>

# To do

1.  [ ] Add docstrings
2.  [ ] Add tests to pre-commit


<a id="orgd17c0df"></a>

# Description


<a id="org798f791"></a>

# Input


<a id="org3964172"></a>

# Output


<a id="org53d5c42"></a>

# Usage


<a id="org2f8d5f5"></a>

## `uv`

    uv run -m boilerplate.main


<a id="orga55d1a2"></a>

## FastAPI

Launch with `uv`:

    uv run uvicorn boilerplate.api:app --reload


<a id="org7e5ce88"></a>

### POST query

    curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
      -H "Content-Type: application/json" \
      -d '{"name":"Amine","age":44}'


<a id="org3e9a511"></a>

### Get query

[http://127.0.0.1:8000/yob?current<sub>year</sub>=2025&name=Amine&age=25](http://127.0.0.1:8000/yob?current_year=2025&name=Amine&age=25)


<a id="org5971a3e"></a>

### Browser

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

