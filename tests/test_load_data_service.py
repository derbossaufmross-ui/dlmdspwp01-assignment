from pathlib import Path

import pandas as pd

from src.models.database_models import create_database
from src.services.load_data import DataLoaderService


def _write_csv(path: Path, header: list[str], rows: list[list[float]]) -> None:
    df = pd.DataFrame(rows, columns=header)
    df.to_csv(path, index=False)


def test_data_loader_service_loads_csv_into_db(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    _write_csv(
        data_dir / "train.csv",
        ["X", "Y1", "Y2", "Y3", "Y4"],
        [[0.0, 1.0, 2.0, 3.0, 4.0], [1.0, 2.0, 3.0, 4.0, 5.0]],
    )
    _write_csv(
        data_dir / "ideal.csv",
        ["X", "Y1", "Y2"],
        [[0.0, 1.1, 2.1], [1.0, 2.1, 3.1]],
    )

    engine = create_database(str(tmp_path / "project.db"))
    service = DataLoaderService(engine=engine, data_dir=data_dir)

    training_df, ideal_df = service.load_all()

    assert list(training_df.columns) == ["x", "y1", "y2", "y3", "y4"]
    assert list(ideal_df.columns) == ["x", "y1", "y2"]

    train_db = pd.read_sql("SELECT * FROM training_data ORDER BY x", con=engine)
    ideal_db = pd.read_sql("SELECT * FROM ideal_functions ORDER BY x", con=engine)
    assert len(train_db) == 2
    assert len(ideal_db) == 2
