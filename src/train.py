from __future__ import annotations

from pathlib import Path

from .data import load_iris_dataframe
from .model import train_and_save_model


def main() -> None:
	artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
	X, y = load_iris_dataframe()
	model_path, val_acc = train_and_save_model(X, y, artifacts_dir)
	print(f"[train] Model saved to: {model_path}")
	print(f"[train] Validation accuracy: {val_acc:.4f}")


if __name__ == "__main__":
	main()


