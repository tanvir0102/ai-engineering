"""Restore workspace/ from workspace_seed/. Run this between demos."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from core._shared import reset_workspace

if __name__ == "__main__":
    reset_workspace()
