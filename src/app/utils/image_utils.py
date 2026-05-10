import cv2
import numpy as np


def decode_image(image_bytes: bytes):
    """
    Convert uploaded image bytes into an OpenCV image.
    """
    image_array = np.frombuffer(image_bytes, np.uint8)
    # decode the image bytes into an OpenCV image
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ValueError("Could not decode image.")

    return image