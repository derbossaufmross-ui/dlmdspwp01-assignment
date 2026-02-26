<<<<<<< HEAD
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

## Run
```bash
python -m src.main
```

## Test
```bash
pytest -q
```
=======
# dlmdspwp01-assignment
>>>>>>> e4edee69ba4d37c262560c48ecc510451d1e5495
