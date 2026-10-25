import pathlib

CODE_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = CODE_DIR.parent
DATASET_DIR = PROJECT_ROOT / "dataset"
MANIFEST_OUTPUT_PATH = CODE_DIR / "manifest.json"
SUPPORTED_EXTENSIONS = {"csv", "json", "sql", "log", "txt"}
MAX_RESOLUTION_PASSES = 3
TARGET_OUTPUT_PATH = DATASET_DIR / "output.csv"
AUDIT_BASELINE_TIMESTAMP = "2026-10-25 00:00:00"