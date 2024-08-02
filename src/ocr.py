import pytesseract


def detect_rotation(image_path):
    """
    This can detect rotation of 90 degrees, 180 degrees, and 270 degrees,
    but an error occurs when tilting at 30 degrees.
    """
    osd = pytesseract.image_to_osd(image_path)
    angle = int(osd.split("Rotate: ")[1].split("\n")[0])
    return angle


def extract_text(image):
    return pytesseract.image_to_string(image, config="--oem 1 -l jpn")
