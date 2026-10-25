from analysis.policy import PolicyEngine

def test_policy_engine_empty(tmp_path):
    engine = PolicyEngine(tmp_path)
    result = engine.evaluate_compliance("any_path.csv", {"type": "arbitrary"})
    assert result["is_allowed"] is False