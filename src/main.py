import argparse
import os

import cv2
from pytesseract import TesseractError

from extractor import JapaneseTextExtractor
from image_processing import detect_skew, rotate_image, warpAffine_rotaion
from ocr import detect_ocr_rotation, extract_text


def save_image(image, directory, filename):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Define the full path for the output file
    file_path = os.path.join(directory, filename)

    # Save the image
    cv2.imwrite(file_path, image)


def get_rotate_image(image):
    rotation_angle = detect_ocr_rotation(image)
    print(f"Detected rotation angle: {rotation_angle}")
    if rotation_angle != 0:
        rotated_image = rotate_image(image, rotation_angle)
        save_image(rotated_image, "output", "rotated_image2.png")
        return rotated_image
    return image


def display(extractor):
    # Extract specific items from text
    print(f"Name: {extractor.name()}")
    print(f"Expiration Date: {extractor.expiration_date()}")
    print(f"Sign: {extractor.sign()}")
    print(f"Number: {extractor.number()}")
    print(f"Birth Day: {extractor.birth_day()}")
    print(f"Sex: {extractor.sex()}")
    print(f"Qualified Day: {extractor.qualified_day()}")
    print(f"Issued Day: {extractor.issued_day()}")
    print(f"Address: {extractor.address()}")
    print(f"Insurer Number: {extractor.insurer_number()}")


def main():
    # Parse arguments
    parser = argparse.ArgumentParser(description="pytesseract tool")
    parser.add_argument("image_path", type=str, help="path to the input image file")
    args = parser.parse_args()
    image_path = args.image_path
    print(f"Image path: {image_path}")

    # Read image
    image = cv2.imread(image_path)

    # Binarize the image
    # FIXME: after executing, pytesseract can't detect text
    # binary_image = binarize_image(image)
    # save_image(binary_image, 'output', 'binary_image.png')

    # Deskew the image
    # FIXME: Invalid number of channels in input image
    # deskewed_image = deskew_image(image)
    # save_image(deskewed_image, "output", "deskewed_image.png")

    # Detect the rotation angle
    rotation_angle = detect_skew(image)
    print(f"Detected rotation angle: {rotation_angle}")

    # Rotate the image to correct orientation
    if rotation_angle != 0.0:
        rotated_image = warpAffine_rotaion(image, rotation_angle, 1.0)
        save_image(rotated_image, "output", "rotated_image.png")
    else:
        rotated_image = image

    # Image may be upside down OCR wise
    # may occur error when background has noise
    try:
        rotated_image = get_rotate_image(rotated_image)
    except TesseractError as e:
        print(f"Failed to call detect_ocr_rotation: {e}")
        # sys.exit(f"Failed to call detect_ocr_rotation: {e}")
        # WIP: remove background
        # no_bg_image = remove_background(rotated_image)
        # save_image(no_bg_image, "output", "no_bg_image.png")

    # Extract text using Tesseract
    text = extract_text(rotated_image)
    print(f"Extracted text: \n{text}")

    # TODO: if there are no extracted items, try to ratate 180 degree then try to extract
    # Reverse image if key items are None
    extractor = JapaneseTextExtractor(text)
    if extractor.expiration_date() is None:
        # reverse 180 degree
        rotated_image = warpAffine_rotaion(rotated_image, 180, 1.0)
        save_image(rotated_image, "output", "rotated_image3.png")
        text = extract_text(rotated_image)
        print(f"Extracted text: \n{text}")
        extractor = JapaneseTextExtractor(text)

    # print all
    display(extractor)


if __name__ == "__main__":
    main()
