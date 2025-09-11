
# Table of Contents

1.  [To do](#org72ed5e2)
2.  [Description](#orgf088149)
3.  [Input](#orgc025973)
4.  [Output](#org328692d)
5.  [Usage](#org2f7cfd9)
    1.  [`uv`](#orgfcfe7db)
    2.  [FastAPI](#org2e766a4)
        1.  [POST query](#orgfbad250)
        2.  [GET query](#org75d51cb)
        3.  [Browser](#org5c27e34)



<a id="org72ed5e2"></a>

# To do

1.  [ ] Add docstrings
2.  [ ] Add tests to pre-commit
3.  [ ] Interchange `age` and `yob`.


<a id="orgf088149"></a>

# Description


<a id="orgc025973"></a>

# Input


<a id="org328692d"></a>

# Output


<a id="org2f7cfd9"></a>

# Usage


<a id="orgfcfe7db"></a>

## `uv`

    uv run -m boilerplate.main


<a id="org2e766a4"></a>

## FastAPI

Launch with `uv`:

    uv run uvicorn boilerplate.api:app --reload


<a id="orgfbad250"></a>

### POST query

    curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
      -H "Content-Type: application/json" \
      -d '{"name":"Olof","age":1958}'


<a id="org75d51cb"></a>

### GET query

[`http://127.0.0.1:8000/yob?current_year=2025&name=Olof&yob=1958`](http://127.0.0.1:8000/yob?current_year=2025&name=Olof&yob=1958)


<a id="org5c27e34"></a>

### Browser

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

