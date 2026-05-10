import easyocr
# Load once when the app starts, not for every request.
reader = easyocr.Reader(["en"], gpu=False)

ALLOWED_PLATE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÄÖÜ- "

def run_ocr(image) -> tuple[str, float]:
    """
    Runs OCR on a cropped license plate image.
    Returns recognized text and average confidence.
    """
    # Use easyocr to read text from the image, restricting to allowed characters.
    results = reader.readtext(
        image,
        detail=1,
        allowlist=ALLOWED_PLATE_CHARS,
    )

    if not results:
        return "", 0.0

    texts = []
    confidences = []

    for _, text, confidence in results:
        texts.append(text)
        confidences.append(confidence)
        
    combined_text = " ".join(texts)
    avg_confidence = sum(confidences) / len(confidences)

    return combined_text, avg_confidence