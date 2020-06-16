# Skills Problem Solving using Python

This is a test to check your skills in Problem Solving, Basic Mathematical knowledge as well as Python programing language

# Prerequisites
- [Python >= 3.7](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/) (_used to consistently create and manage the virtualenv_)
- [Docker](https://docs.docker.com/get-docker/)

# Project Structure Overview
```
- setup.py
+ notebook (jupyter notebook with initial algorithm design)
  └───| - irr-with-numpy.ipynb
+ src (main source code)
  └───| + in_memory_db
      | + irr
      | - dextra.py
+ tests (unit tests using pytest framework)
  └───| + in_memory_db
      | + irr
      | - test_common.py
```

# How to Run Main Application

1. Install Pipenv:
    - `pip install pipenv`

2. Hit `run.py`:
    - `pipenv run python src/run.py`

## Arguments

| Option | Description |
|--------|-------------|
| -h     | Provide useful help messages |
| -d     | Set 'D' day (expected format: `dd/mm/yyyy`, default: when empty, is defined as the previous day from first cash flow) |

# How to Run Unit Tests (using PyTest framework)

1. Install Pipenv:
    - `pip install pipenv`

2. Run the script:
    - `./scripts/run_tests.sh`

## Code Coverage Report

Please refer to [this link](htmlcov/index.html). (alternatively, when running the unit tests the coverage is also reported)

- Code Coverage: *84%*

- Report:

    | Name |                                    Stmts |  Miss  | Cover   | Missing           |
    | --------------------------------------- |------ |------- |-------- |------------------ |
    | src/__init__.py                         | 0     | 0      | 100%    |                   |
    | src/dextra.py                           | 65    | 3      | 95%     | 91, 119-120       |
    | src/in_memory_db/__init__.py            | 3     | 0      | 100%    |                   |
    | src/in_memory_db/in_memory_db.py        | 14    | 5      | 64%     | 9, 13, 17, 21, 25 |
    | src/in_memory_db/in_memory_db_lite.py   | 41    | 3      | 93%     | 40, 49, 58        |
    | src/irr/__init__.py                     | 2     | 0      | 100%    |                   |
    | src/irr/irr.py                          | 30    | 2      | 93%     | 62, 75            |
    | src/run.py                              | 15    | 15     | 0%      | 3-25              |
    | *TOTAL*                                 | *170* | *28*   | *84%*   |                   |

# How to Build the Docker Image

1. Run the script (refer to arguments in the header):
    - `./scripts/build.sh`

- By default, the script will generate an image tagged as `dextra/big-data-python:latest`.
