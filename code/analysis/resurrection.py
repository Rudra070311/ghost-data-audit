import pathlib
from typing import List, Dict, Any

class ResurrectionDetector:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)

    def detect_resurrection(self, deletion_request: Dict[str, Any], timeline_events: List[Dict[str, Any]]) -> Dict[str, Any]:
        request_time = deletion_request.get("request_date", deletion_request.get("timestamp", ""))
        resurrected = False
        leaking_sources = []

        for event in timeline_events:
            event_time = event.get("timestamp", event.get("date", event.get("event_time", "")))
            if event_time and request_time and event_time > request_time:
                resurrected = True
                source = event.get("source_path", "unknown_source")
                if source not in leaking_sources:
                    leaking_sources.append(source)

        return {
            "resurrected": resurrected,
            "leaking_sources": leaking_sources,
            "reason": f"Active user data observed in sources after deletion window: {leaking_sources}" if resurrected else "No post-deletion synchronization activity found"
        }