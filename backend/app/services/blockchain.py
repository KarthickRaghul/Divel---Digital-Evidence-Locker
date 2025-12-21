from app.core.config import settings
from web3 import Web3
import hashlib
import json

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
        self.contract = None
        if self.w3.is_connected() and settings.BLOCKCHAIN_CONTRACT_ADDRESS:
            # We would load ABI here. For now, we assume simple interface or mock.
            # self.contract = self.w3.eth.contract(...)
            pass
        
        # Local file-based ledger for MVP durability if blockchain is down/not configured
        self.ledger_file = "local_blockchain_ledger.json"
        
    def calculate_hash(self, file_content: bytes) -> str:
        return hashlib.sha256(file_content).hexdigest()

    def store_hash_on_chain(
        self, 
        case_id: str, 
        evidence_id: str, 
        file_hash: str, 
        file_type: str, 
        uploader_role: str, 
        previous_hash: str = None
    ):
        """
        Stores the hash and metadata on the blockchain.
        Returns the transaction hash.
        """
        if self.w3.is_connected() and self.contract:
            # Implementing real transaction stub
            # tx = self.contract.functions.anchorEvidence(
            #     evidence_id, case_id, file_hash, file_type, uploader_role, previous_hash or ""
            # ).transact(...)
            # return tx.hex()
            return "0xMOCK_TRANSACTION_HASH_ON_CHAIN"
        
        # Fallback to local ledger
        entry = {
            "case_id": case_id,
            "evidence_id": evidence_id,
            "hash": file_hash,
            "file_type": file_type,
            "uploader_role": uploader_role,
            "previous_hash": previous_hash,
            "timestamp": str(datetime.now())
        }
        self._append_to_ledger(entry)
        return f"0xLOCAL_LEDGER_{hashlib.md5(file_hash.encode()).hexdigest()}"

    def verify_integrity(self, evidence_id: str, computed_hash: str) -> dict:
        """
        Verifies if the computed hash matches the stored hash on chain.
        Returns a dictionary with comprehensive verification details.
        """
        # In a real app, we query the contract.
        # Here we look up our local ledger.
        
        record = self._get_record_from_ledger(evidence_id)
        
        if not record:
            return {
                "verified": False,
                "status": "NOT_FOUND_ON_CHAIN",
                "details": "Evidence ID not found in the blockchain ledger."
            }
            
        stored_hash = record.get("hash")
        is_valid = (stored_hash == computed_hash)
        
        return {
            "verified": is_valid,
            "status": "VERIFIED" if is_valid else "TAMPERED",
            "details": "Hash matches blockchain record." if is_valid else "Hash Mismatch! File may have been altered.",
            "blockchain_record": {
                "timestamp": record.get("timestamp"),
                "uploader_role": record.get("uploader_role"),
                "stored_hash": stored_hash
            }
        }

    def _append_to_ledger(self, entry):
        try:
            with open(self.ledger_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        
        data.append(entry)
        
        with open(self.ledger_file, 'w') as f:
            json.dump(data, f)
            
    def _get_hash_from_ledger(self, evidence_id):
        # Deprecated: Use _get_record_from_ledger
        record = self._get_record_from_ledger(evidence_id)
        return record.get("hash") if record else None

    def _get_record_from_ledger(self, evidence_id):
        try:
            with open(self.ledger_file, 'r') as f:
                data = json.load(f)
                for entry in data:
                    if entry.get("evidence_id") == evidence_id:
                        return entry
        except FileNotFoundError:
            return None
        return None

from datetime import datetime
blockchain = BlockchainService()
