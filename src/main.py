from src.models.database_models import create_database
from src.services.load_data import DataLoaderService
from src.services.ideal_selector import IdealSelector
from src.services.map_test_data import TestDataMapper
from src.services.visualize import VisualizationService
"""
Orchestrates the full workflow:
1) create DB, 2) load training+ideal, 3) select best ideal functions (Least Squares),
4) map test data line-by-line with sqrt(2) criterion, 5) create Bokeh visualization.
"""

def main() -> None:
    engine = create_database()

    # 1) Load training + ideal into DB
    loader = DataLoaderService(engine)
    training_df, ideal_df = loader.load_all()

    # 2) Select best ideal functions via Least Squares (SSE)
    selector = IdealSelector()
    selections = selector.select(training_df, ideal_df)

    print("Selected ideal functions:")
    for s in selections:
        print(f"{s.training_col} -> {s.ideal_col} | SSE={s.sse:.4f} | max_dev={s.max_dev_train_ideal:.4f}")

    # 3) Map test data line-by-line and store in DB
    mapper = TestDataMapper(engine)
    n_mapped = mapper.map_and_store(selections)
    print(f"Mapped test rows written to DB: {n_mapped}")

    # 4) Visualize
    viz = VisualizationService(engine)
    html_path = viz.create(selections)
    print(f"Visualization saved to: {html_path}")


if __name__ == "__main__":
    main()

