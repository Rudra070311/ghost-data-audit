import pathlib
from identity.resolver import IdentityResolver, IdentityProfile

def test_identity_resolver_expansion():
    manifest = {"user_identities.csv": {"file_type": "csv", "status": "SUCCESS"}}
    profile = IdentityProfile(request_id="REQ_1", seed_email="seed@test.com", seed_account_id="acc_1")
    data_dir = pathlib.Path(__file__).parent.parent / "dataset"
    resolver = IdentityResolver(data_dir)
    
    assert "seed@test.com" in resolver.get_emails()
    assert "acc_1" in resolver.get_account_ids()
    assert "REQ_1" == resolver.get_request_id()