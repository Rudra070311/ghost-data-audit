import pathlib
import re
from datetime import datetime
from typing import List, Dict, Any
from identity.resolver import IdentityProfile
from ingestion.media import UnstructuredReader

class TimelineReconstructor:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)

    def extract_date_from_filename(self, filename: str) -> str:
        match = re.search(r'(\d{4})_?(\d{2})_?(\d{2})|(\d{8})', filename)
        if match:
            groups = match.groups()
            if groups[0] and groups[1] and groups[2]:
                return f"{groups[0]}-{groups[1]}-{groups[2]} 00:00:00"
            elif groups[3]:
                g = groups[3]
                return f"{g[:4]}-{g[4:6]}-{g[6:8]} 00:00:00"
        return "1970-01-01 00:00:00"

    def normalize_timestamp(self, ts_value: Any, filename: str) -> str:
        if not ts_value:
            return self.extract_date_from_filename(filename)
        
        ts_str = str(ts_value).strip()
        try:
            clean_ts = re.sub(r'(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}).*', r'\1 \2', ts_str)
            dt = datetime.strptime(clean_ts, "%Y-%m-%d %H:%M:%S")
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            pass

        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%m/%d/%Y"):
            try:
                dt = datetime.strptime(ts_str, fmt)
                return dt.strftime("%Y-%m-%d 00:00:00")
            except ValueError:
                continue

        return self.extract_date_from_filename(filename)

    def build_timeline(self, profile: IdentityProfile, manifest: Dict[str, Any]) -> List[Dict[str, Any]]:
        events = []
        
        for rel_path, info in manifest.items():
            full_path = self.data_dir / rel_path
            file_type = info["file_type"]
            if info["status"] != "SUCCESS":
                continue

            try:
                reader = UnstructuredReader(full_path, file_type)
                filename = full_path.name
                for item in reader.read_items():
                    if isinstance(item, dict):
                        is_match = ((item.get("email") in profile.emails) or(item.get("account_id") in profile.account_ids) or(item.get("phone_number") in profile.phone_numbers))
                        if is_match:
                            raw_ts = item.get("timestamp", item.get("date", item.get("event_time")))
                            norm_ts = self.normalize_timestamp(raw_ts, filename) 
                            event_entry = {**item}
                            event_entry["timestamp"] = norm_ts
                            event_entry["source_path"] = rel_path
                            events.append(event_entry)
            except Exception as e:
                print(f"Error reading {rel_path}: {e}")
                continue
            
        events.sort(key=lambda x: x.get("timestamp", "1970-01-01 00:00:00"))
        return events