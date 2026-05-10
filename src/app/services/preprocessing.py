import cv2


def preprocess_plate_for_ocr(image):
    """
    Mild preprocessing only.
    Avoid strong thresholding because it can make stickers look like digits.

    This step can be tweaked to find the right balance between improving OCR 
    accuracy and not over-processing the image.
    """
    image = cv2.resize(
        image,
        None,
        fx=2,
        fy=2,
        interpolation=cv2.INTER_CUBIC,
    )
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Mild contrast improvement
    #gray = cv2.equalizeHist(gray)

    return gray