from typing import Dict, Any, List

class DecisionEngine:
    @staticmethod
    def evaluate_verdict(deletion_request: Dict[str, Any], timeline_events: List[Dict[str, Any]], resurrection_results: Dict[str, Any]) -> Dict[str, Any]:
        if not deletion_request or not (deletion_request.get("request_id") or deletion_request.get("email")):
            return {
                "verdict": "NOT_APPLICABLE",
                "remediation_steps": []
            }

        if resurrection_results.get("resurrected") or len(timeline_events) > 0:
            remediation_steps = []
            sources = resurrection_results.get("leaking_sources", [])
            if not sources:
                sources = ["unredacted_secondary_storage"]
                
            for idx, source in enumerate(sources, 1):
                remediation_steps.append(f"{idx}. Purge, overwrite, or anonymize user token rows from target source ledger: {source}")
                
            return {
                "verdict": "INCOMPLETE",
                "remediation_steps": remediation_steps
            }

        return {
            "verdict": "COMPLETE",
            "remediation_steps": []
        }