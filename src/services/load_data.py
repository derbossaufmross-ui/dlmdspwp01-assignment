"""
Load CSV data into the SQLite database using pandas + SQLAlchemy.

Loads:
- training data (train.csv) into table 'training_data'
- ideal functions (ideal.csv) into table 'ideal_functions'
"""
from pathlib import Path

import pandas as pd
from sqlalchemy import Engine

from src.exceptions import DataLoadError
from src.services.base_service import BaseService


def load_training_data(engine: Engine, csv_path: str | Path) -> None:
    """Load training CSV into table `training_data`."""
    try:
        df = pd.read_csv(csv_path).rename(columns=str.lower)
    except (OSError, pd.errors.ParserError) as exc:
        raise DataLoadError(f"Could not read training data from '{csv_path}'.") from exc

    try:
        df.to_sql("training_data", con=engine, if_exists="replace", index=False)
    except Exception as exc:
        raise DataLoadError("Could not write table 'training_data'.") from exc


def load_ideal_functions(engine: Engine, csv_path: str | Path) -> None:
    """Load ideal-function CSV into table `ideal_functions`."""
    try:
        df = pd.read_csv(csv_path).rename(columns=str.lower)
    except (OSError, pd.errors.ParserError) as exc:
        raise DataLoadError(f"Could not read ideal functions from '{csv_path}'.") from exc

    try:
        df.to_sql("ideal_functions", con=engine, if_exists="replace", index=False)
    except Exception as exc:
        raise DataLoadError("Could not write table 'ideal_functions'.") from exc


def load_all(engine: Engine, data_dir: str | Path = "data") -> None:
    """Load both required CSV files into SQLite tables."""
    data_dir = Path(data_dir)
    train_path = data_dir / "train.csv"
    ideal_path = data_dir / "ideal.csv"

    if not train_path.exists():
        raise FileNotFoundError(f"Missing file: {train_path}")
    if not ideal_path.exists():
        raise FileNotFoundError(f"Missing file: {ideal_path}")

    load_training_data(engine, train_path)
    load_ideal_functions(engine, ideal_path)


class DataLoaderService(BaseService):
    """Service wrapper around the data-loading functions."""

    def __init__(self, engine: Engine, data_dir: str | Path = "data") -> None:
        super().__init__(engine)
        self.data_dir = Path(data_dir)

    def load_all(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Load CSVs into DB and return normalized DataFrames for downstream steps."""
        load_all(self.engine, self.data_dir)

        training_df = pd.read_csv(self.data_dir / "train.csv").rename(columns=str.lower)
        ideal_df = pd.read_csv(self.data_dir / "ideal.csv").rename(columns=str.lower)
        return training_df, ideal_df
