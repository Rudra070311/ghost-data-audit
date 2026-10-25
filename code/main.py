import json
import csv
import pathlib
from config import DATASET_DIR, MANIFEST_OUTPUT_PATH, TARGET_OUTPUT_PATH
from ingestion.manifest import Manifest
from ingestion.media import UnstructuredReader
from identity.resolver import IdentityResolver
from analysis.timeline import TimelineReconstructor
from analysis.policy import PolicyEngine
from analysis.resurrection import ResurrectionDetector
from analysis.decision import DecisionEngine
from remediation.planner import RemediationPlanner

def run_pipeline():
    print("GHOST DATA AUDITOR")

    print("\n[Step 1/6] Discovering and analyzing raw evidence corpus files...")
    manifest = Manifest.build_manifest(DATASET_DIR)
    
    for rel_path, info in list(manifest.items()):
        if info["status"] == "UNSUPPORTED":
            continue
        
        full_path = DATASET_DIR / rel_path
        file_type = info["file_type"]
        item_count = 0
        errors = []
        status = "SUCCESS"

        try:
            reader = UnstructuredReader(full_path, file_type)
            for _ in reader.read_items():
                item_count += 1
        except Exception as e:
            status = "FAILED"
            errors.append(str(e))

        manifest = Manifest.record_result(
            manifest=manifest,
            source_path=rel_path,
            status=status,
            item_count=item_count,
            errors=errors
        )
    
    Manifest.save_manifest(manifest, MANIFEST_OUTPUT_PATH)
    print(f"✓ Ingestion coverage footprint complete. Logged to {MANIFEST_OUTPUT_PATH}")
    print("\n[Step 2/6] Spin up underlying agent evaluation modules...")
    resolver = IdentityResolver(DATASET_DIR)
    reconstructor = TimelineReconstructor(DATASET_DIR)
    policy_engine = PolicyEngine(DATASET_DIR)
    resurrection_detector = ResurrectionDetector(DATASET_DIR)
    planner = RemediationPlanner(DATASET_DIR)

    requests_path = DATASET_DIR / "deletion_requests.csv"
    if not requests_path.is_file():
        raise FileNotFoundError(f"Missing core deletion requests file entry: {requests_path}")
        
    deletion_requests = []
    with requests_path.open("r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        
        cleaned_fieldnames = {k: k.encode('utf-8').decode('utf-8-sig').strip().lower() for k in reader.fieldnames} if reader.fieldnames else {}
        
        for row in reader:
            clean_row = {cleaned_fieldnames.get(k, k): v for k, v in row.items()}
            deletion_requests.append(clean_row)
    print(f"Successfully loaded {len(deletion_requests)} active audit tasks.")

    print("\n[Step 4/6] Executing multi-pass identification and forensic tracing...")
    predictions_log = []

    for req in deletion_requests:
        req_id = req.get("request_id")
        seed_email = req.get("email", "")
        seed_account = req.get("account_id", "")
        print(f"  → Inspecting {req_id} | Seed: {seed_email or seed_account}")

        profile = resolver.resolve_identity(request_id=req_id, email=seed_email, account_id=seed_account, manifest=manifest)
        timeline = reconstructor.build_timeline(profile, manifest)
        res_results = resurrection_detector.detect_resurrection(req, timeline)
        decision = DecisionEngine.evaluate_verdict(req, timeline, res_results)
        verdict = decision["verdict"]
        steps_blueprint = planner.generate_plan(req_id, verdict, timeline, res_results)

        predictions_log.append({
            "request_id": req_id,
            "deletion_status": verdict,
            "steps_json": json.dumps(steps_blueprint)
        })

    print("\n[Step 5/6] Serializing final compliant audit record sheet output data...")
    
    with TARGET_OUTPUT_PATH.open("w", newline="", encoding="utf-8") as outfile:
        fieldnames = ["request_id", "deletion_status", "steps_json"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for prediction in predictions_log:
            writer.writerow(prediction)

    print(f"Absolute target submission document printed successfully: {TARGET_OUTPUT_PATH}")
    print("\n[Step 6/6] Summary execution framework overview metrics:")
    
    summary = Manifest.validate_coverage(manifest)
    for key, count in summary.items():
        label = key.replace("_", " ").title()
        print(f"  • {label}: {count}")
        
    print("READY FOR ZIP")

if __name__ == "__main__":
    run_pipeline()