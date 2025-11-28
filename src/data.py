from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.datasets import load_iris


def load_iris_dataframe() -> Tuple[pd.DataFrame, pd.Series]:
	"""Load Iris dataset as DataFrame (features) and Series (target)."""
	iris = load_iris(as_frame=True)
	X = iris.data
	y = iris.target
	return X, y


