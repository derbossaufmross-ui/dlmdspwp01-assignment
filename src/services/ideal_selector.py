from __future__ import annotations

from dataclasses import dataclass
from typing import List

import numpy as np
import pandas as pd

from src.exceptions import IdealSelectionError


@dataclass(frozen=True)
class IdealSelection:
    """Selection result for one training function."""

    training_col: str
    ideal_col: str
    sse: float
    max_dev_train_ideal: float


class IdealSelector:
    """
    Selects the best ideal function for each training function by minimizing
    the sum of squared y-deviations (Least Squares / SSE).
    """

    def __init__(self, training_cols: List[str] | None = None):
        """Create a selector for a list of training columns."""
        self.training_cols = training_cols or ["y1", "y2", "y3", "y4"]

    def select(self, training_df: pd.DataFrame, ideal_df: pd.DataFrame) -> List[IdealSelection]:

        """Return one best-fitting ideal function per training function by minimum SSE."""

        training_df = training_df.rename(columns=str.lower)
        ideal_df = ideal_df.rename(columns=str.lower)

        if "x" not in training_df.columns or "x" not in ideal_df.columns:
            raise IdealSelectionError("Both DataFrames must contain column 'x'.")

        for c in self.training_cols:
            if c not in training_df.columns:
                raise IdealSelectionError(f"Missing training column: {c}")

        ideal_cols = [c for c in ideal_df.columns if c.startswith("y") and c != "x"]
        if not ideal_cols:
            raise IdealSelectionError("No ideal columns found (expected y1..y50).")

        merged = pd.merge(
            training_df[["x"] + self.training_cols],
            ideal_df[["x"] + ideal_cols],
            on="x",
            how="inner",
            validate="one_to_one",
            suffixes=("_train", "_ideal"),
        )
        if merged.empty:
            raise IdealSelectionError("No overlapping x-values between training and ideal data.")

        # after merge, training columns become e.g. y1_train because ideal has y1 too
        
        train_cols_m = [f"{c}_train" if f"{c}_train" in merged.columns else c for c in self.training_cols]

        # ideal columns after merge: prefer *_ideal if present, but keep original name for output
        ideal_cols_m: List[str] = []
        ideal_cols_out: List[str] = []
        for c in ideal_cols:
            if f"{c}_ideal" in merged.columns:
                ideal_cols_m.append(f"{c}_ideal")
                ideal_cols_out.append(c)
            elif c in merged.columns:
                ideal_cols_m.append(c)
                ideal_cols_out.append(c)

        ideal_matrix = merged[ideal_cols_m].to_numpy(dtype=float)

        selections: List[IdealSelection] = []
        for tcol, tcol_m in zip(self.training_cols, train_cols_m):
            t = merged[tcol_m].to_numpy(dtype=float).reshape(-1, 1)
            diffs = ideal_matrix - t

            sse_per_ideal = np.sum(diffs ** 2, axis=0)
            max_dev_per_ideal = np.max(np.abs(diffs), axis=0)

            best_idx = int(np.argmin(sse_per_ideal))
            selections.append(
                IdealSelection(
                    training_col=tcol,
                    ideal_col=ideal_cols_out[best_idx],
                    sse=float(sse_per_ideal[best_idx]),
                    max_dev_train_ideal=float(max_dev_per_ideal[best_idx]),
                )
            )

        return selections
