from evaluation.metrics import QualityMetrics

def test_schema_validation():
    row = {
        "request_id": "REQ_1",
        "deletion_status": "COMPLETE",
        "reremediation_steps": []
    }
    assert QualityMetrics.validate_schema(row) is True
