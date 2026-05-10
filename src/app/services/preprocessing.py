import cv2
from matplotlib.pyplot import gray


def preprocess_plate_for_ocr(image):
    """
    Mild preprocessing only.
    Avoid strong thresholding because it can make stickers look like digits.

    This step can be tweaked to find the right balance between improving OCR 
    accuracy and not over-processing the image.
    """
    resized_image = cv2.resize(
        image,
        (400, 100)
    )
    # Convert to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Mild contrast improvement
    gray = cv2.equalizeHist(gray)

    # Mild noise reduction
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    return blurred