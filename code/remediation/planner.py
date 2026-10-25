import pathlib
from typing import List, Dict, Any

class RemediationPlanner:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)

    def generate_plan(self, request_id: str, verdict: str, timeline_events: List[Dict[str, Any]], resurrection_results: Dict[str, Any]) -> List[Dict[str, Any]]:
        steps = []
        if verdict != "INCOMPLETE":
            return steps

        leaking_sources = resurrection_results.get("leaking_sources", [])
        if not leaking_sources:
            leaking_sources = ["unredacted_secondary_storage"]

        for idx, source in enumerate(leaking_sources, 1):
            steps.append({
                "step_number": idx,
                "action": "PURGE_AND_REDACT",
                "target_source": str(source),
                "description": f"Purge, overwrite, or anonymize user token rows from target source ledger: {source}",
                "dependencies": [idx - 1] if idx > 1 else []
            })
            
        return steps