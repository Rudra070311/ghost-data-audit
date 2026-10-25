import pathlib
from ingestion.manifest import Manifest
from ingestion.media import UnstructuredReader

def run_pipeline():
    code_dir = pathlib.Path(__file__).resolve().parent
    project_root = code_dir.parent
    dataset_dir = project_root / "dataset"
    manifest_output = code_dir / "manifest.json"
    manifest = Manifest.build_manifest(dataset_dir)
    
    print(f"Initializing Scan")
    print(f"Dir: {dataset_dir}")
    print(f"Found {len(manifest)}files\n")

    for rel_path, info in list(manifest.items()):
        full_path = dataset_dir / rel_path
        file_type = info["file_type"]

        if info["status"] == "UNSUPPORTED":
            print(f"[-] Skip: Unsupported file extension type [{file_type.upper()}] -> {rel_path}")
            continue

        print(f"[+] Processing [{file_type.upper()}]: {rel_path}")
        
        item_count = 0
        errors = []
        status = "SUCCESS"

        try:
            reader = UnstructuredReader(full_path, file_type)
            
            for i in reader.read_items():
                item_count += 1
               
        except Exception as e:
            status = "FAILED"
            errors.append(str(e))
            print(f"Execution Error: {e}")

        manifest = Manifest.record_result(
            manifest=manifest,
            source_path=rel_path,
            status=status,
            item_count=item_count,
            errors=errors
        )

    print("Summary")
    summary = Manifest.validate_coverage(manifest)
    for key, count in summary.items():
        label = key.replace("_", " ").title()
        print(f" => {label}: {count}")

    Manifest.save_manifest(manifest, manifest_output)

if __name__ == "__main__":
    run_pipeline()