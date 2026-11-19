from fastapi import APIRouter, UploadFile, File

router = APIRouter(tags=["Parsing"])

@router.post('/pdf')
async def parse_pdf(file: UploadFile | None = File(None)):
    return {
        "status": "not_implemented",
        "filename": file.filename if file else None,
    }