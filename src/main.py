import argparse
import os

import cv2

from image_processing import (
    detect_skew,  # binarize_image, deskew_image
    rotate_image,
    warpAffine_rotaion,
)
from ocr import detect_rotation, extract_text


def save_image(image, directory, filename):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the full path for the output file
    file_path = os.path.join(directory, filename)

    # Save the image
    cv2.imwrite(file_path, image)


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="pytesseract tool")
    parser.add_argument("image_path", type=str, help="path to the input image file")
    args = parser.parse_args()
    image_path = args.image_path
    print(f"Image path: {image_path}")

    # Read image
    image = cv2.imread(image_path)

    # Image processing
    # - Step 1: Binarize the image
    # FIXME: after executing, pytesseract can't detect text
    # binary_image = binarize_image(image)
    # save_image(binary_image, 'output', 'binary_image.png')

    # - Step 2: Deskew the image
    # FIXME: Invalid number of channels in input image
    # deskewed_image = deskew_image(image)
    # save_image(deskewed_image, "output", "deskewed_image.png")

    # - Step 3: Detect the rotation angle
    rotation_angle = detect_skew(image)
    print(f"Detected rotation angle: {rotation_angle}")

    # - Step 4: Rotate the image to correct orientation
    if rotation_angle != 0.0:
        rotated_image = warpAffine_rotaion(image, rotation_angle, 1.0)
        save_image(rotated_image, "output", "rotated_image.png")
    else:
        rotated_image = image

    # it may be upside down OCR wise
    rotation_angle = detect_rotation(rotated_image)
    print(f"Detected rotation angle: {rotation_angle}")
    if rotation_angle != 0:
        rotated_image = rotate_image(image, rotation_angle)
        save_image(rotated_image, "output", "rotated_image2.png")

    # Extract text using Tesseract
    text = extract_text(rotated_image)
    print(f"Extracted text: \n{text}")


if __name__ == "__main__":
    main()
