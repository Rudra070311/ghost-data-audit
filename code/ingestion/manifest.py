import json
import hashlib
import pathlib
from typing import Dict, Any, List

class Manifest:
    @staticmethod
    def build_manifest(root_dir: pathlib.Path) -> Dict[str, Any]:
        manifest = {}
        
        for path in root_dir.rglob("*"):
            if path.is_dir():
                continue
            
            hasher = hashlib.sha256()
            with pathlib.Path(path).open("rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            content_hash = hasher.hexdigest()
            
            file_type = pathlib.Path(path).suffix
            if file_type != ".csv" and file_type != ".sql" and file_type != ".json" and file_type != ".png":
                raise ValueError(f"Unsupported file type: {file_type}. Only CSV, SQL, JSON, and PNG files are supported.")

            rel_path = str(path.relative_to(root_dir)).replace("\\", "/")
            manifest[str(rel_path)] = {
                "source_id": f"src_{content_hash}",
                "source_path": str(rel_path),
                "file_type": file_type,
                "sha256": content_hash,
                "size_bytes": pathlib.Path(path).stat().st_size,
                "status": "PENDING",
                "items_extracted": 0,
                "errors": []
            }

        return manifest



    @staticmethod
    def record_result(manifest: Dict[str, Any], source_path: str, status: str, item_count: int, errors: List[str] = None) -> Dict[str, Any]:
        source_path = str(source_path)
        if errors is None:
            errors = []
        update_data = {
            "status": status,
            "items_extracted": item_count,
            "errors": errors
        }
        
        return {**manifest, source_path: {**manifest.get(source_path, {}), **update_data}}

    @staticmethod
    def validate_coverage(manifest: Dict[str, Any]) -> Dict[str, int]:
        total_files = len(manifest)
        success_files = sum(1 for data in manifest.values() if data.get("status") == "SUCCESS")
        pending_files = sum(1 for data in manifest.values() if data.get("status") == "PENDING")
        partial_files = sum(1 for data in manifest.values() if data.get("status") == "PARTIAL")
        failed_files = sum(1 for data in manifest.values() if data.get("status") == "FAILED")
        unsupported_files = sum(1 for data in manifest.values() if data.get("status") == "UNSUPPORTED")

        return {
            "total_files": total_files,
            "success_files": success_files,
            "pending_files": pending_files,
            "partial_files": partial_files,
            "failed_files": failed_files,
            "unsupported_files": unsupported_files
        }

    @staticmethod
    def save_manifest(manifest: Dict[str, Any], output_path: pathlib.Path) -> None:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
        print(f"Manifest saved to {output_path}")
