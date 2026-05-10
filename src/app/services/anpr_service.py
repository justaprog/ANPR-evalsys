import time
from app.utils.image_utils import decode_image
from app.services.crop import crop_license_text_area
from app.services.ocr import run_ocr
from app.services.postprocess import (clean_plate_text, 
                                      build_german_plate_from_tokens, 
                                      is_valid_german_plate,
                                      )

def recognize_plate_ocr_only(
    image_bytes: bytes,
    filename: str,
    content_type: str,
) -> dict:
    """
    OCR-only baseline.
    Input should be a cropped license plate image.
    """
    start_time = time.perf_counter()

    image = decode_image(image_bytes)
    text_area = crop_license_text_area(image)

    tokens, confidence = run_ocr(text_area)
    raw_text = " ".join(tokens)
    
    # clean and correct the OCR output to build a plausible German plate text
    corrected_text = build_german_plate_from_tokens(tokens)
    cleaned_text = clean_plate_text(corrected_text)

    valid_format = is_valid_german_plate(cleaned_text)

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return {
        "filename": filename,
        "content_type": content_type,
        "plate_text": cleaned_text,
        "raw_text": raw_text,
        "confidence": round(confidence, 4),
        "valid_format": valid_format,
        "latency_ms": latency_ms,
        "engine": "easyocr_ocr_only_v1",
    }