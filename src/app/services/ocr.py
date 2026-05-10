import easyocr
import numpy as np

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
    # NOTE: This step is super important for performance, improve results significantly.
    # But be careful with over-processing - too much sharpening or noise reduction 
    # can also hurt results. e.g: 2 stickers -> 8 and D, which is not a part of the license plate text.
    # NOTE: OCR can read non-license characters like stickers, which can be a problem for postprocessing.
    processed_image = preprocess_plate_for_ocr(image)
    # Use easyocr to read text from the image, restricting to allowed characters.
    # param_sets to avoid merging separate characters into one box, which can cause incorrect OCR results.
    param_sets = [
        {"width_ths": 0.50, "ycenter_ths": 0.5, "height_ths": 0.5, "add_margin": 0.1},
        {"width_ths": 0.20, "ycenter_ths": 0.4, "height_ths": 0.4, "add_margin": 0.05},
        {"width_ths": 0.10, "ycenter_ths": 0.3, "height_ths": 0.3, "add_margin": 0.0},
        {"width_ths": 0.05, "ycenter_ths": 0.3, "height_ths": 0.3, "add_margin": 0.0},
        {"width_ths": 0.01, "ycenter_ths": 0.2, "height_ths": 0.2, "add_margin": 0.0},
    ]

    results = reader.readtext(
        processed_image,
        detail=1,
        allowlist=ALLOWED_PLATE_CHARS,
        # use the first param set
        **param_sets[4]
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
    sorted_results = sort_results_left_to_right(results)
    
    tokens = []
    confidences = []

    for bbox, text, confidence in sorted_results:
        tokens.append(text)
        confidences.append(confidence)
        
    avg_confidence = sum(confidences) / len(confidences)

    return tokens, avg_confidence

def sort_results_left_to_right(results):
    return sorted(results, key=lambda item: bbox_center(item[0])[0])

def bbox_center(bbox):
    """
    Example BBOX format from easyocr:
    BBOX: [[np.int32(114), np.int32(38)], 
            [np.int32(188), np.int32(38)], 
            [np.int32(188), np.int32(112)], 
            [np.int32(114), np.int32(112)]]
    """
    xs = [float(point[0]) for point in bbox]
    ys = [float(point[1]) for point in bbox]

    x_center = sum(xs) / len(xs)
    y_center = sum(ys) / len(ys)

    return x_center, y_center


def bbox_height(bbox):
    ys = [float(point[1]) for point in bbox]
    return max(ys) - min(ys)