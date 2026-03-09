
# DLMDSPWP01 Project (Programming with Python)

## What this project does
This program solves the IU assignment workflow:
- load training + ideal data into SQLite
- select 4 best ideal functions (least squares / SSE)
- map test points to those 4 functions using the `sqrt(2)` deviation rule
- save mapping results and generate a Bokeh visualization

## Why I structured it this way
- I split logic into services so each step can be tested independently.
- I kept the SQL model definitions in one place (`src/models/database_models.py`) so schema changes are easy.
- I used pandas for CSV/joins because this task is very table-oriented.

## Design tradeoffs
- Mapping reads `test.csv` line-by-line (as requested), but ideal data is loaded into memory once for speed.
- I used a small float tolerance for matching x-values to avoid precision issues between CSV sources.
- Visualization focuses on clarity over styling: mapped points encode deviation by both size and color.

## Limitations / TODO
- Current tests are strong on service behavior but still not a full CLI/integration test of error exits.
- No command-line argument parsing yet (paths are still defaults unless changed in code).
- Logging is minimal (plain prints in `main.py`).

## Setup (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -r requirements.txt

## Run
python -m src.main

## Test
python -m pytest -q

## Input data (CSV)
Create folder `data/` in the repository root and place:
- data/train.csv
- data/ideal.csv
- data/test.csv

