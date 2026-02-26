from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.models.database_models import create_database
from src.services.ideal_selector import IdealSelection
from src.services.map_test_data import TestDataMapper


def test_map_and_store_persists_accepted_test_points(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    pd.DataFrame({"x": [0.0, 1.0], "y1": [1.0, 2.0]}).to_csv(data_dir / "ideal.csv", index=False)
    pd.DataFrame({"x": [0.0, 1.0], "y": [1.0, 2.4]}).to_csv(data_dir / "test.csv", index=False)

    engine = create_database(str(tmp_path / "project.db"))
    mapper = TestDataMapper(
        engine=engine,
        test_csv_path=str(data_dir / "test.csv"),
        ideal_csv_path=str(data_dir / "ideal.csv"),
    )

    selections = [IdealSelection("y1", "y1", sse=0.0, max_dev_train_ideal=0.3)]
    mapped = mapper.map_and_store(selections)

    assert mapped == 2

    with engine.connect() as conn:
        rows = conn.execute(text("SELECT x, y, delta_y, ideal_no FROM test_mapping ORDER BY x")).fetchall()

    assert len(rows) == 2
    assert rows[0].ideal_no == 1
