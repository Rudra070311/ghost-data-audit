from typing import List, Dict, Any

class QualityMetrics:
    @staticmethod
    def calculate_accuracy(evaluation_report: Dict[str, Any]) -> float:
        total = evaluation_report.get("total_evaluated", 0)
        if total == 0:
            return 0.0
        return float(evaluation_report.get("matches", 0) / total)

    @staticmethod
    def validate_schema(output_row: Dict[str, Any]) -> bool:
        required_keys = ["request_id", "deletion_status", "reremediation_steps"]
        return all(key in output_row for key in required_keys)
