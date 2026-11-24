"""Compatibility entry point for the heuristic experiment; accepts --export."""
from pathlib import Path
import runpy


if __name__ == "__main__":
    runpy.run_path(str(Path(__file__).resolve().parent / "experiments/heuristic/run.py"),
                  run_name="__main__")
