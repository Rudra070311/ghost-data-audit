from analysis.decision import DecisionEngine

def test_decision_complete():
    req = {"request_id": "REQ_1", "email": "test@test.com"}
    res = DecisionEngine.evaluate_verdict(req, [], {"resurrected": False})
    assert res["verdict"] == "COMPLETE"

def test_decision_incomplete():
    req = {"request_id": "REQ_1", "email": "test@test.com"}
    res = DecisionEngine.evaluate_verdict(req, [{"timestamp": "2026-10-02"}], {"resurrected": True, "leaking_sources": ["db.sql"]})
    assert res["verdict"] == "INCOMPLETE"