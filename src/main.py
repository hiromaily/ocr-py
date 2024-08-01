import argparse
import os

import cv2

from image_processing import rotate_image  # binarize_image, deskew_image
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
    parser = argparse.ArgumentParser(description="pytesseract tool")
    parser.add_argument("image_path", type=str, help="path to the input image file")
    args = parser.parse_args()
    image_path = args.image_path
    print(f"Image path: {image_path}")

    # Read image
    image = cv2.imread(image_path)

    # Step 1: Binarize the image
    # FIXME: after executing, pytesseract can't detect text
    # binary_image = binarize_image(image)
    # save_image(binary_image, 'output', 'binary_image.png')

    # Step 2: Detect the rotation angle
    rotation_angle = detect_rotation(image_path)
    print(f"Detected rotation angle: {rotation_angle}")

    # Step 3: Rotate the image to correct orientation
    rotated_image = rotate_image(image, -rotation_angle)
    save_image(rotated_image, "output", "rotated_image.png")

    # Step 4: Deskew the image
    # FIXME: Invalid number of channels in input image
    # deskewed_image = deskew_image(rotated_image)

    # Step 5: Extract text using Tesseract
    text = extract_text(rotated_image)
    print(f"Extracted text: \n{text}")


if __name__ == "__main__":
    main()
