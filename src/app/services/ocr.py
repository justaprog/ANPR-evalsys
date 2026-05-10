import easyocr

from app.services.preprocessing import preprocess_plate_for_ocr

# Load once when the app starts, not for every request.
reader = easyocr.Reader(["en"], gpu=False)

ALLOWED_PLATE_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÄÖÜ- "

def run_ocr(image) -> tuple[list[str], float]:
    """
    Runs OCR on a cropped license plate image.
    Returns recognized text and average confidence.
    """
    # Preprocess the image to improve OCR accuracy.
    # NOTE: This step is super important for performance. 
    # improve confidence from 0.2589 to 0.8662 on plate_02.png for example.
    # But be careful with over-processing - too much sharpening or noise reduction 
    # can also hurt results. e.g: 2 stickers -> 8 and D, which is not a part of the license plate text.
    # NOTE: OCR can read non-license characters like stickers, which can be a problem for postprocessing.
    processed_image = preprocess_plate_for_ocr(image)
    # Use easyocr to read text from the image, restricting to allowed characters.
    
    results = reader.readtext(
        processed_image,
        detail=1,
        allowlist=ALLOWED_PLATE_CHARS,
    )

    # For debugging: print OCR results
    # TODO: remove or comment out in production
    for bbox, text, confidence in results:
        print("TEXT:", text)
        print("CONF:", confidence)
        print("BBOX:", bbox)
        print()

    if not results:
        return [], 0.0
    # Sort results left-to-right based on bounding box x-coordinates to maintain correct text order.
    results = sort_results_left_to_right(results)

    tokens = []
    confidences = []

    for bbox, text, confidence in results:
        tokens.append(text)
        confidences.append(confidence)
        
    combined_text = " ".join(tokens)
    avg_confidence = sum(confidences) / len(confidences)

    return tokens, avg_confidence

def get_x_center(bbox: list[tuple[float, float]]) -> float:
    """
    Example BBOX format from easyocr:
    BBOX: [[np.int32(114), np.int32(38)], 
            [np.int32(188), np.int32(38)], 
            [np.int32(188), np.int32(112)], 
            [np.int32(114), np.int32(112)]]
    """
    xs = [float(point[0]) for point in bbox]
    return sum(xs) / len(xs)

def sort_results_left_to_right(results):
    return sorted(results, key=lambda item: get_x_center(item[0]))