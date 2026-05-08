import time

def recognize_plate_dummy(filename: str, content_type: str) -> dict:
    """
    Temporary dummy ANPR service.
    Later we replace this with:
    image -> detection -> crop -> OCR -> postprocessing.
    """
    start_time = time.perf_counter()

    # Simulate result for now
    plate_text = "B AB 1234"
    confidence = 0.91
    valid_format = True

    latency_ms = int((time.perf_counter() - start_time) * 1000)

    return {
        "filename": filename,
        "content_type": content_type,
        "plate_text": plate_text,
        "confidence": confidence,
        "valid_format": valid_format,
        "latency_ms": latency_ms,
        "engine": "dummy_v1",
    }