import cv2

from image_processing import binarize_image, rotate_image  # deskew_image
from ocr import detect_rotation, extract_text


def main():
    # TODO: from argument
    image_path = "../images/sample_.png"
    image = cv2.imread(image_path)

    # Step 1: Binarize the image
    binary_image = binarize_image(image)

    # Step 2: Detect the rotation angle
    rotation_angle = detect_rotation(image_path)
    print(f"Detected rotation angle: {rotation_angle}")

    # Step 3: Rotate the image to correct orientation
    rotated_image = rotate_image(binary_image, -rotation_angle)

    # Step 4: Deskew the image
    # FIXME: Invalid number of channels in input image
    # deskewed_image = deskew_image(rotated_image)

    # Step 5: Extract text using Tesseract
    text = extract_text(rotated_image)
    print(text)


if __name__ == "__main__":
    main()
