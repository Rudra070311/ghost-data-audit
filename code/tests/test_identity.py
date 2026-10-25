import pathlib
from identity.resolver import IdentityResolver, IdentityProfile

def test_identity_resolver_expansion():
    manifest = {"user_identities.csv": {"file_type": "csv", "status": "SUCCESS"}}
    profile = IdentityProfile(request_id="REQ_1", seed_email="seed@test.com", seed_account_id="acc_1")
    
    assert "seed@test.com" in profile.emails
    assert "acc_1" in profile.account_ids
