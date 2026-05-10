import re

LETTER_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ"
DIGIT_CHARS = "0123456789"
# Common OCR confusions
TO_DIGIT = {
    "O": "0",
    "I": "1",
    "L": "1",
    "Z": "2",
    "S": "5",
    "B": "8",
    "G": "6",
}

TO_LETTER = {
    "0": "O",
    "1": "I",
    "2": "Z",
    "5": "S",
    "8": "B",
    "6": "G",
}

def clean_plate_text(text: str) -> str:
    """
    Normalize OCR output for license plates.
    """
    text = text.upper()
    text = text.replace(" ", "")
    text = text.replace("-", "")

    allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ÄÖÜ"
    return "".join(char for char in text if char in allowed_chars)


def is_valid_german_plate(text: str) -> bool:
    """
    Simple German-style plate validation.

    Simplified German plate:
        city code: 1-3 letters
        serial:    1-2 letters
        number:    1-4 digits
        optional:  E or H suffix

    Examples:
    B AB 1234  -> BAB1234
    M XY 987   -> MXY987

    This is intentionally simplified for the MVP.
    For more details on German plate formats, see: 
    https://en.wikipedia.org/wiki/Vehicle_registration_plates_of_Germany#Format_and_legal_requirements
    """
    # explain: The regex checks for:
    # - 1 to 3 uppercase letters (including ÄÖÜ) at the start
    # - followed by 1 to 2 uppercase letters
    # - followed by 1 to 4 digits
    # - optionally ending with 'E' or 'H' for electric or historic plates
    pattern = r"^[A-ZÄÖÜ]{1,3}[A-ZÄÖÜ]{1,2}[0-9]{1,4}[EH]?$"

    return bool(re.match(pattern, text))

def correct_as_letters(text: str) -> str:
    result = []

    for char in text.upper():
        if char.isalpha() or char in "ÄÖÜ":
            result.append(char)
        elif char in TO_LETTER:
            result.append(TO_LETTER[char])

    return "".join(result)


def correct_as_digits(text: str) -> str:
    result = []

    for char in text.upper():
        if char.isdigit():
            result.append(char)
        elif char in TO_DIGIT:
            result.append(TO_DIGIT[char])

    return "".join(result)


def build_german_plate_from_tokens(tokens: list[str]) -> str:
    """
    Example:
    ["SHA", "02", "268"] -> "SHAOZ268"
    """

    if len(tokens) == 3:
        city = correct_as_letters(tokens[0])
        serial = correct_as_letters(tokens[1])
        number = correct_as_digits(tokens[2])

        return city + serial + number

    # fallback for unexpected cases
    return " ".join(tokens)