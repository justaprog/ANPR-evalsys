def crop_license_text_area(image):
    """
    Crop the image to focus on the main license plate text area, removing EU strip
    """
    height, width = image.shape[:2]

    # Remove EU strip on the left
    x1 = int(width * 0.1)

    return image[:, x1:]