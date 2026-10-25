import pathlib
from typing import Dict, Any, Set
from ingestion.media import UnstructuredReader

class IdentityProfile:
    def __init__(self, request_id: str, seed_email: str = None, seed_account_id: str = None):
        self.request_id = request_id
        self.account_ids: Set[str] = {seed_account_id} if seed_account_id else set()
        self.emails: Set[str] = {seed_email} if seed_email else set()
        self.phone_numbers: Set[str] = set()
        self.provenance: Dict[str, str] = {}
        if seed_email: self.provenance[seed_email] = "Seed deletion request"
        if seed_account_id: self.provenance[seed_account_id] = "Seed deletion request"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "account_ids": list(self.account_ids),
            "emails": list(self.emails),
            "phone_numbers": list(self.phone_numbers),
            "provenance": self.provenance
        }

class IdentityResolver:
    def __init__(self, data_dir: pathlib.Path):
        self.data_dir = pathlib.Path(data_dir)

    def resolve_identity(self, request_id: str, email: str, account_id: str, manifest: Dict[str, Any]) -> IdentityProfile:
        profile = IdentityProfile(request_id, seed_email=email, seed_account_id=account_id)
        profile.provenance[email] = "Seed deletion request"
        profile.provenance[account_id] = "Seed deletion request"
        
        for rel_path, info in manifest.items():
            full_path = self.data_dir / rel_path
            file_type = info["file_type"]

            if info["status"] != "SUCCESS":
                continue

            try:
                reader = UnstructuredReader(full_path, file_type)
                for item in reader.read_items():
                    if isinstance(item, dict):
                        has_matching_email = item.get("email") in profile.emails
                        has_matching_account = item.get("account_id") in profile.account_ids
                        has_matching_phone = item.get("phone_number") in profile.phone_numbers

                        if has_matching_email or has_matching_account or has_matching_phone:
                            if "email" in item and item["email"]:
                                if item["email"] not in profile.emails:
                                    profile.emails.add(item["email"])
                                    profile.provenance[item["email"]] = f"Linked via record match in {rel_path}"
                            if "account_id" in item and item["account_id"]:
                                if item["account_id"] not in profile.account_ids:
                                    profile.account_ids.add(item["account_id"])
                                    profile.provenance[item["account_id"]] = f"Linked via record match in {rel_path}"
                            if "phone_number" in item and item["phone_number"]:
                                if item["phone_number"] not in profile.phone_numbers:
                                    profile.phone_numbers.add(item["phone_number"])
                                    profile.provenance[item["phone_number"]] = f"Linked via record match in {rel_path}"                            
            except Exception as e:
                print(f"Error processing {rel_path}: {e}")
        return profile
