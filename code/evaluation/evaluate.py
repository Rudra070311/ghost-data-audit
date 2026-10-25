import pathlib
import csv
from typing import Dict, Any, List
from evaluation.metrics import QualityMetrics

class EvaluationWorkflow:
    def __init__(self, dataset_dir: pathlib.Path):
        self.dataset_dir = pathlib.Path(dataset_dir)

    def load_expected_outputs(self, filename: str = "sample_output.csv") -> Dict[str, str]:
        expected = {}
        expected_path = self.dataset_dir / filename
        if expected_path.is_file():
            with expected_path.open("r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    req_id = row.get("request_id")
                    status = row.get("deletion_status")
                    if req_id and status:
                        expected[req_id] = status
        return expected

    def run_evaluation(self, predictions: List[Dict[str, Any]]) -> Dict[str, Any]:
        expected = self.load_expected_outputs()
        report = {"total_evaluated": len(predictions), "matches": 0, "failures": []}
        
        for pred in predictions:
            req_id = pred.get("request_id")
            pred_status = pred.get("deletion_status")
            exp_status = expected.get(req_id)
            
            if exp_status:
                if pred_status == exp_status:
                    report["matches"] += 1
                else:
                    report["failures"].append({
                        "request_id": req_id,
                        "expected": exp_status,
                        "predicted": pred_status
                    })
                    
        return report