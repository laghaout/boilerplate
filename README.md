
# Table of Contents

1.  [To do](#org1176121)
2.  [Description](#org0afc338)
3.  [Input](#orgcfb0f3f)
4.  [Output](#org64df2bd)
5.  [Usage](#orgf517d81)
    1.  [`uv`](#orge6920fa)
    2.  [FastAPI](#org8c2ff7a)
        1.  [POST query](#orgc1e9ddf)
        2.  [GET query](#orgc1c962e)
        3.  [Browser](#org9db5370)



<a id="org1176121"></a>

# To do

1.  [ ] Add docstrings
2.  [ ] Add tests to pre-commit
3.  [ ] Interchange `age` and `yob`.


<a id="org0afc338"></a>

# Description


<a id="orgcfb0f3f"></a>

# Input


<a id="org64df2bd"></a>

# Output


<a id="orgf517d81"></a>

# Usage


<a id="orge6920fa"></a>

## `uv`

    uv run -m boilerplate.main


<a id="org8c2ff7a"></a>

## FastAPI

Launch with `uv`:

    uv run uvicorn boilerplate.api:app --reload


<a id="orgc1e9ddf"></a>

### POST query

    curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
      -H "Content-Type: application/json" \
      -d '{"name":"Amine","age":44}'


<a id="orgc1c962e"></a>

### GET query

[`http://127.0.0.1:8000/yob?current_year=2025&name=Amine&age=25`](http://127.0.0.1:8000/yob?current_year=2025&name=Amine&age=25)


<a id="org9db5370"></a>

### Browser

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

