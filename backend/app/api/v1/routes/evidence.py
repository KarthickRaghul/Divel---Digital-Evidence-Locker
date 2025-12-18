from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
async def upload_evidence(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "status": "received"
    }
