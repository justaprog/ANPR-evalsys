from fastapi import FastAPI, File, UploadFile, HTTPException
from app.schemas import RecognitionResponse
from app.services.anpr_service import recognize_plate_dummy

app = FastAPI(
    title="ANPR Evaluation API",
    description="Prototype API for Automatic Number Plate Recognition evaluation.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "anpr-evaluation-api",
    }


@app.post("/recognize", response_model=RecognitionResponse)
async def recognize_plate(file: UploadFile = File(...)) -> dict:
    """
    Accepts an uploaded vehicle image and returns a license plate recognition result.
    Currently uses a dummy service.
    """

    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(
            status_code=400, # Bad Request
            detail="Only JPEG, PNG, and WEBP images are supported.",
        )

    # For now we only read the file to verify that upload works.
    # Later we will pass these bytes to OpenCV / OCR.
    image_bytes = await file.read()

    if len(image_bytes) == 0:
        raise HTTPException(
            status_code=400, # Bad Request
            detail="Uploaded file is empty.",
        )

    result = recognize_plate_dummy(
        filename=file.filename or "unknown",
        content_type=file.content_type or "unknown",
    )

    return result