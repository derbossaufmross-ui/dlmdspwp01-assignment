from __future__ import annotations

import csv
from collections.abc import Iterable

import numpy as np
import pandas as pd
from sqlalchemy import MetaData, Table, insert
from sqlalchemy.engine import Engine

from src.exceptions import MappingError
from src.services.ideal_selector import IdealSelection


class TestDataMapper:
    """Map each test point to one selected ideal function and persist accepted rows."""
    __test__ = False

    def __init__(
        self,
        engine: Engine,
        test_csv_path: str = "data/test.csv",
        ideal_csv_path: str = "data/ideal.csv",
        x_tolerance: float = 1e-9,
    ) -> None:
        """Create mapper with CSV paths and x-value tolerance for float matching."""
        self.engine = engine
        self.test_csv_path = test_csv_path
        self.ideal_csv_path = ideal_csv_path
        self.x_tolerance = x_tolerance

    def map_and_store(self, selections: Iterable[IdealSelection]) -> int:
        """Map test rows and store accepted rows into `test_mapping`."""
        ideal_df = pd.read_csv(self.ideal_csv_path).rename(columns=str.lower)
        ideal_df["x"] = pd.to_numeric(ideal_df["x"])
        ideal_df = ideal_df.set_index("x")
        ideal_x = ideal_df.index.to_numpy(dtype=float)

        # candidates: (ideal_col, ideal_no, threshold)
        candidates: list[tuple[str, int, float]] = []
        for s in selections:
            ideal_col = s.ideal_col.lower()
            if ideal_col not in ideal_df.columns:
                raise MappingError(f"Ideal column '{ideal_col}' not found in ideal CSV.")

            ideal_no = int(ideal_col.lstrip("y"))
            threshold = float(s.max_dev_train_ideal) * np.sqrt(2.0)
            candidates.append((ideal_col, ideal_no, threshold))

        mapping_table = self._resolve_mapping_table()

        mapped_count = 0
        with self.engine.begin() as conn:
            # For this assignment run, overwrite previous mapping results.
            conn.execute(mapping_table.delete())

            # Assignment requires line-by-line processing for test data.
            with open(self.test_csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    x = float(row["x"])
                    y = float(row["y"])

                    x_used = self._resolve_x_value(x, ideal_x)
                    if x_used is None:
                        continue

                    best_delta: float | None = None
                    best_ideal_no: int | None = None
                    best_threshold: float | None = None

                    for ideal_col, ideal_no, threshold in candidates:
                        yi = float(ideal_df.at[x_used, ideal_col])
                        delta = abs(y - yi)

                        if best_delta is None or delta < best_delta:
                            best_delta = delta
                            best_ideal_no = ideal_no
                            best_threshold = threshold

                    if best_delta is None or best_ideal_no is None or best_threshold is None:
                        continue

                    if best_delta <= best_threshold:
                        conn.execute(
                            insert(mapping_table).values(
                                x=x,
                                y=y,
                                delta_y=float(best_delta),
                                ideal_no=best_ideal_no,
                            )
                        )
                        mapped_count += 1

        return mapped_count

    def _resolve_mapping_table(self) -> Table:
        """Resolve and validate the mandatory `test_mapping` table schema."""
        md = MetaData()
        md.reflect(bind=self.engine)

        mapping_table = md.tables.get("test_mapping")
        if mapping_table is None:
            raise MappingError("Table 'test_mapping' not found.")

        required = {"x", "y", "delta_y", "ideal_no"}
        cols = {c.name.lower() for c in mapping_table.columns}
        if not required.issubset(cols):
            raise MappingError("Table 'test_mapping' must contain: x, y, delta_y, ideal_no.")

        return mapping_table

    def _resolve_x_value(self, x: float, ideal_x_values: np.ndarray) -> float | None:
        """Resolve x-value with exact match first and tolerance-based fallback."""
        if x in ideal_x_values:
            return x

        # CSV float parsing can differ slightly; fall back to tolerance match.
        close = np.isclose(ideal_x_values, x, atol=self.x_tolerance, rtol=0.0)
        if not np.any(close):
            return None

        return float(ideal_x_values[np.flatnonzero(close)[0]])
