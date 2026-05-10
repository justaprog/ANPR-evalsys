import cv2


def preprocess_plate_for_ocr(image):
    # Enlarge image first. OCR often works better on larger text.
    image = cv2.resize(
        image,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC,
    )

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve local contrast
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )
    gray = clahe.apply(gray)

    # Denoise slightly
    gray = cv2.GaussianBlur(gray, (3, 3), 0)

    # Sharpen
    sharpened = cv2.addWeighted(gray, 1.5, gray, -0.5, 0)

    return sharpened