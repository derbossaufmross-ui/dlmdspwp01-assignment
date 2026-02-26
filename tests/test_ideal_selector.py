import pandas as pd
from src.services.ideal_selector import IdealSelector


def test_ideal_selector_picks_min_sse():
    # simple controlled data
    training = pd.DataFrame(
        {"x": [1, 2, 3], "y1": [1, 2, 3], "y2": [0, 0, 0], "y3": [1, 1, 1], "y4": [2, 2, 2]}
    )

    ideal = pd.DataFrame(
        {
            "x": [1, 2, 3],
            "y1": [1, 2, 3],   # perfect for y1
            "y2": [9, 9, 9],   # bad
            "y3": [0, 0, 0],   # perfect for y2
            "y4": [1, 1, 1],   # perfect for y3
            "y5": [2, 2, 2],   # perfect for y4
        }
    )

    sel = IdealSelector().select(training, ideal)
    mapping = {s.training_col: s.ideal_col for s in sel}

    assert mapping["y1"] == "y1"
    assert mapping["y2"] == "y3"
    assert mapping["y3"] == "y4"
    assert mapping["y4"] == "y5"
