from pathlib import Path

import pandas as pd

from src.models.database_models import create_database
from src.services.ideal_selector import IdealSelection
from src.services.visualize import VisualizationService


def test_visualization_service_creates_html_file(tmp_path: Path) -> None:
    db_path = tmp_path / "project.db"
    engine = create_database(str(db_path))

    pd.DataFrame({"x": [0.0, 1.0], "y1": [1.0, 2.0], "y2": [2.0, 3.0], "y3": [3.0, 4.0], "y4": [4.0, 5.0]}).to_sql(
        "training_data", con=engine, if_exists="replace", index=False
    )
    pd.DataFrame({"x": [0.0, 1.0], "y1": [1.1, 2.1]}).to_sql("ideal_functions", con=engine, if_exists="replace", index=False)
    pd.DataFrame({"x": [0.0], "y": [1.05], "delta_y": [0.05], "ideal_no": [1]}).to_sql(
        "test_mapping", con=engine, if_exists="replace", index=False
    )

    test_csv_path = tmp_path / "test.csv"
    pd.DataFrame({"x": [0.0, 1.0], "y": [1.0, 2.0]}).to_csv(test_csv_path, index=False)

    out_path = tmp_path / "viz.html"
    service = VisualizationService(engine=engine, out_path=str(out_path), test_csv_path=str(test_csv_path))

    selections = [IdealSelection("y1", "y1", sse=0.0, max_dev_train_ideal=0.1)]

    result_path = service.create(selections)

    assert result_path == str(out_path)
    assert out_path.exists()
    assert out_path.stat().st_size > 0
