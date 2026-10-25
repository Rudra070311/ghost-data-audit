import pathlib
import csv
from typing import Dict, Any, List

class PolicyEngine:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)
        self.rules: List[Dict[str, str]] = []
        self.load_rules()

    def load_rules(self):
        rules_path = self.data_dir / "deletion_rules.csv"
        if rules_path.is_file():
            try:
                with rules_path.open(mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    self.rules = [row for row in reader]
            except Exception as e:
                print(f"Error loading deletion rules configuration: {e}")

    def evaluate_compliance(self, file_path: str, record: Dict[str, Any]) -> Dict[str, Any]:
        is_allowed = False
        reason = "No explicit retention policy rule matched this record profile"
        normalized_path = str(file_path).replace("\\", "/")

        for rule in self.rules:
            rule_path = rule.get("file_path", "").replace("\\", "/")
            system_type = rule.get("system", "")
            action = rule.get("action", rule.get("action_required", ""))
            path_match = rule_path and rule_path in normalized_path
            system_match = system_type and system_type.lower() in normalized_path.lower()
            
            if path_match or system_match:
                if action in ["ALLOW", "RETAIN", "LEGAL_HOLD"]:
                    is_allowed = True
                    reason = f"Record allowed due to retention rule: {rule}"
                    break
                elif action in ["DENY", "DELETE", "PURGE"]:
                    is_allowed = False
                    reason = f"Record explicitly forbidden due to purge rule: {rule}"
                    break

        return {"is_allowed": is_allowed, "reason": reason}