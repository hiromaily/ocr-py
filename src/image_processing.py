import cv2
import numpy as np


def binarize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return binary_image


# # Bug version
# def rotate_image(image, angle):
#     (h, w) = image.shape[:2]
#     center = (w // 2, h // 2)
#     M = cv2.getRotationMatrix2D(center, angle, 1.0)
#     rotated = cv2.warpAffine(
#         image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
#     )
#     return rotated
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    # Compute the new bounding dimensions of the image
    new_w = int(h * abs(np.sin(np.radians(angle))) + w * abs(np.cos(np.radians(angle))))
    new_h = int(h * abs(np.cos(np.radians(angle))) + w * abs(np.sin(np.radians(angle))))
    # Compute the center of the new image
    # center = (new_w // 2, new_h // 2)

    # Get the rotation matrix for rotating and scaling the image
    M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)

    # Adjust the rotation matrix to account for the translation
    M[0, 2] += (new_w - w) / 2
    M[1, 2] += (new_h - h) / 2

    # Perform the rotation
    rotated = cv2.warpAffine(
        image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
    )
    return rotated


def deskew_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    return rotate_image(image, angle)
