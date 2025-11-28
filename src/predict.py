from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np

from .model import load_model


def main() -> None:
	artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
	model_path = artifacts_dir / "model.joblib"

	if not model_path.exists():
		print("[predict] Model not found. Run: python -m src.train")
		return

	model = load_model(model_path)

	sample = np.array(
		[
			[5.1, 3.5, 1.4, 0.2],
			[6.7, 3.1, 4.7, 1.5],
			[6.3, 3.3, 6.0, 2.5],
		]
	)
	preds = model.predict(sample)
	print(f"[predict] Predictions: {preds.tolist()}")


if __name__ == "__main__":
	main()


