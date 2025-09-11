#+TITLE: Boilerplate README

* To do
1. [ ] Add docstrings
2. [ ] Add tests to pre-commit
3. [ ] Interchange =age= and =yob=.
* Description
* Input
* Output
* Usage
** =uv=
#+begin_src python
uv run -m boilerplate.main
#+end_src
** FastAPI
Launch with =uv=:
#+begin_src bash :results output
uv run uvicorn boilerplate.api:app --reload
#+end_src
*** POST query
#+begin_src bash :results output
curl -X POST "http://127.0.0.1:8000/yob?current_year=2025" \
  -H "Content-Type: application/json" \
  -d '{"name":"Olof","age":1958}'
#+end_src
*** GET query
[[http://127.0.0.1:8000/yob?current_year=2025&name=Olof&yob=1958][=http://127.0.0.1:8000/yob?current_year=2025&name=Olof&yob=1958=]]
*** Browser
[[http://127.0.0.1:8000/docs][=http://127.0.0.1:8000/docs=]]
