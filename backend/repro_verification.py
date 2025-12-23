import sys
import os
import json
from unittest.mock import MagicMock

# Add current directory to path
sys.path.append(os.getcwd())

# Mock app.core.config
class MockSettings:
    BLOCKCHAIN_RPC_URL = "http://127.0.0.1:8545"

mock_config = MagicMock()
mock_config.settings = MockSettings()

sys.modules["app.core.config"] = mock_config
sys.modules["pydantic_settings"] = MagicMock() # Mock this too just in case

# Now import blockchain
from app.services.blockchain import blockchain

def run_repro():
    evidence_id = "572388b3-f67a-4970-8504-028e7726cb7c"
    
    print(f"Testing verification for Evidence ID: {evidence_id}")
    
    # 1. Get from Ledger directly (mimic evidence.py logic)
    record = blockchain._get_record_from_ledger(evidence_id)
    if not record:
        print("Record not found in local ledger!")
        return
        
    stored_hash = record.get("hash")
    print(f"Stored Hash in Ledger: {stored_hash}")
    
    # 2. Verify Integrity
    print("Calling blockchain.verify_integrity...")
    result = blockchain.verify_integrity(evidence_id, stored_hash)
    
    print("\nVerification Result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    run_repro()
