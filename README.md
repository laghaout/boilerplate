
# Table of Contents

1.  [To do](#org0776b62)
2.  [Description](#orgb71b047)
3.  [Input](#orgd9fc00e)
4.  [Output](#org9e04f0f)
5.  [Usage](#org4a9d744)
    1.  [Docker](#org6fdb542)
    2.  [`uv`](#org6fab565)
    3.  [TensorBoard](#org706afb6)
    4.  [FastAPI](#org9bdb760)
        1.  [POST query](#org3988002)
        2.  [GET query](#org8c55b4a)
        3.  [Browser](#org4d903dd)



<a id="org0776b62"></a>

# To do

1.  [ ] Include relevant functions from `utilities`
2.  [ ] Add docstrings
3.  [ ] Add tests to pre-commit
4.  [ ] Interchange `age` and `yob`.
5.  [ ] Ability to save and reload
6.  [ ] Add tests
7.  [ ] Add a Dockerfile


<a id="orgb71b047"></a>

# Description


<a id="orgd9fc00e"></a>

# Input


<a id="org9e04f0f"></a>

# Output


<a id="org4a9d744"></a>

# Usage


<a id="org6fdb542"></a>

## Docker

    docker build -t boilerplate .


<a id="org6fab565"></a>

## `uv`

    uv run -m boilerplate.main


<a id="org706afb6"></a>

## TensorBoard

    uv run tensorboard --logdir "output/TensorBoard"


<a id="org9bdb760"></a>

## FastAPI

Launch with `uv`:

    uv run uvicorn boilerplate.api:app --reload


<a id="org3988002"></a>

### POST query

    curl -X 'POST' \
      'http://127.0.0.1:8000/age?current_year=2025' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "name": "Olof",
      "yob": 1958,
      "attributes": [
        "string"
      ],
      "age": 0
    }'


<a id="org8c55b4a"></a>

### GET query

[`http://127.0.0.1:8000/age?current_year=2025&name=Olof&yob=1958`](http://127.0.0.1:8000/age?current_year=2025&name=Olof&yob=1958)


<a id="org4d903dd"></a>

### Browser

[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)

