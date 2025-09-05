
# Table of Contents

1.  [Description](#org0728856)
2.  [Input](#orgd7fa8d3)
3.  [Output](#orgf29f646)
4.  [Usage](#org0a7dfd0)
    1.  [`uv`](#orgb2af6a1)
    2.  [FastAPI](#orgb6a6d39)
        1.  [`uv`](#orge8845e1)
        2.  [`curl`](#org7257cfe)
        3.  [Browser](#org1eb0e5c)



<a id="org0728856"></a>

# Description


<a id="orgd7fa8d3"></a>

# Input


<a id="orgf29f646"></a>

# Output


<a id="org0a7dfd0"></a>

# Usage


<a id="orgb2af6a1"></a>

## `uv`

    uv run -m boilerplate.main


<a id="orgb6a6d39"></a>

## FastAPI


<a id="orge8845e1"></a>

### `uv`

    uv run uvicorn boilerplate.api:app --reload


<a id="org7257cfe"></a>

### `curl`

    curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
      -H "Content-Type: application/json" \
      -d '{"name":"Amine","age":44}'


<a id="org1eb0e5c"></a>

### Browser

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
