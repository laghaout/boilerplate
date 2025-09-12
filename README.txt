#+TITLE: Boilerplate code

* To do
1. [ ] Include relevant functions from =utilities=
2. [ ] Add docstrings
3. [ ] Add tests to pre-commit
4. [ ] Interchange =age= and =yob=.
5. [ ] Ability to save and reload
6. [ ] Add tests
7. [ ] Add a Dockerfile
* Description
* Input
* Output
* Usage
** Docker
#+begin_src bash :results output
docker build -t boilerplate .
#+end_src
** =uv=
#+begin_src bash :results output
uv run -m boilerplate.main
#+end_src
** TensorBoard
#+begin_src bash :results output
uv run tensorboard --logdir "output/TensorBoard"
#+end_src
** FastAPI
Launch with =uv=:
#+begin_src bash :results output
uv run uvicorn boilerplate.api:app --reload
#+end_src
*** POST query
#+begin_src bash :results output
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
#+end_src
*** GET query
[[http://127.0.0.1:8000/age?current_year=2025&name=Olof&yob=1958][=http://127.0.0.1:8000/age?current_year=2025&name=Olof&yob=1958=]]
*** Browser
[[http://127.0.0.1:8000/docs][=http://127.0.0.1:8000/docs=]]
