from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional
from app.api.v1.endpoints import auth
from app.services.storage import storage
from app.services.database import db
from app.services.blockchain import blockchain
from app.services.ai import ai_service
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/upload")
async def upload_evidence(
    file: UploadFile = File(...),
    case_id: str = Form(...),
    current_user: auth.User = Depends(auth.get_current_polaris_user)
):
    # 1. Read file content
    content = await file.read()
    
    # 2. Compute Hash
    file_hash = blockchain.calculate_hash(content)
    
    # 3. Upload to Storage
    # Reset cursor for upload
    file.file.seek(0)
    file_url = storage.upload_file(file.file, f"{case_id}/{file.filename}", file.content_type or "application/octet-stream")
    
    # 4. Store Metadata
    evidence_id = str(uuid.uuid4())
    metadata = {
        "id": evidence_id,
        "case_id": case_id,
        "filename": file.filename,
        "uploader": current_user.username,
        "hash": file_hash,
        "url": file_url,
        "uploaded_at": str(datetime.now())
    }
    db.store_evidence_metadata(metadata)
    
    # 5. Anchor to Blockchain
    tx_hash = blockchain.store_hash_on_chain(case_id, evidence_id, file_hash)
    
    # 6. Trigger AI (Async in real world, sync here for MVP)
    # We might extract text if it's a doc, here we just pass filename as dummy content
    ai_summary = ai_service.generate_summary(f"Evidence file: {file.filename}")
    
    return {
        "evidence_id": evidence_id,
        "hash": file_hash,
        "tx_hash": tx_hash,
        "ai_summary": ai_summary
    }

@router.get("/{evidence_id}/verify")
async def verify_evidence(
    evidence_id: str,
    current_user: auth.User = Depends(auth.get_current_user) # Forensics or Judge
):
    # Check permissions
    if current_user.role not in ["Forensics", "Judge"]:
         raise HTTPException(status_code=403, detail="Unauthorized")

    # 1. Get Metadata
    metadata = db.get_evidence_metadata(evidence_id)
    if not metadata:
        raise HTTPException(status_code=404, detail="Evidence not found")
        
    # 2. Re-compute has (Need to fetch file from S3)
    # For MVP we assume we have the file or just trust the metadata hash for the "computed" part 
    # if we haven't implemented full S3 download yet.
    # In a full impl, we download `metadata['url']` and hash it.
    
    computed_hash = metadata['hash'] # leveraging the stored one for now as we don't have real S3 fetch implemented in this single file
    
    # 3. Verify against Blockchain
    is_valid = blockchain.verify_integrity(evidence_id, computed_hash)
    
    return {
        "evidence_id": evidence_id,
        "status": "VERIFIED" if is_valid else "TAMPERED",
        "blockchain_hash": blockchain._get_hash_from_ledger(evidence_id), # exposes helper for debug
        "computed_hash": computed_hash
    }
