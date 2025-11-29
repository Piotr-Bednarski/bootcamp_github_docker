from __future__ import annotations

from pathlib import Path
from typing import Tuple

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


def ensure_directory(path: Path) -> None:
	"""Create directory if it doesn't exist."""
	path.mkdir(parents=True, exist_ok=True)


def build_pipeline() -> Pipeline:
	"""Create a simple ML pipeline."""
	return Pipeline(
		steps=[
			("scaler", StandardScaler()),
			("clf", LogisticRegression(max_iter=100, n_jobs=3, random_state=36)),
		]
	)


def train_and_save_model(X: pd.DataFrame, y: pd.Series, artifacts_dir: Path) -> Tuple[Path, float]:
	"""Train pipeline and persist to artifacts directory. Returns (model_path, val_accuracy)."""
	ensure_directory(artifacts_dir)

	print("Starting fitting model …")

	X_train, X_val, y_train, y_val = train_test_split(
		X, y, test_size=0.4, random_state=42, stratify=y
	)

	pipeline = build_pipeline()
	pipeline.fit(X_train, y_train)

	y_pred = pipeline.predict(X_val)
	val_acc = accuracy_score(y_val, y_pred)

	model_path = artifacts_dir / "model.joblib"
	joblib.dump(pipeline, model_path)
	return model_path, float(val_acc)


def load_model(model_path: Path):
	"""Load model from disk."""
	return joblib.load(model_path)


