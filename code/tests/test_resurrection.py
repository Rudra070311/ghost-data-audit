from analysis.resurrection import ResurrectionDetector

def test_no_resurrection(tmp_path):
    detector = ResurrectionDetector(tmp_path)
    req = {"request_date": "2026-09-01 00:00:00"}
    timeline = [{"timestamp": "2026-08-15 00:00:00", "source_path": "db.sql"}]
    res = detector.detect_resurrection(req, timeline)
    assert res["resurrected"] is False