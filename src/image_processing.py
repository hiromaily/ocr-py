import cv2
import numpy as np

# from typing_extensions import deprecated


def binarize_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    binary_image = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return binary_image


def detect_skew(image):
    """
    It can detect skew, but it may be upside down OCR wise
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to find edges
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Use Hough Line Transform to detect lines in the image
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    if lines is None:
        return 0  # If no lines are detected, assume no skew

    angles = []

    # Iterate over the detected lines and compute the angles
    for line in lines:
        for rho, theta in line:
            angle = (theta * 180 / np.pi) - 90
            angles.append(angle)

    # Compute the median angle
    skew_angle = np.median(angles)

    return skew_angle


# @deprecated("will be removed")
# def rotate_image(image, angle):
#     """
#     This can rotate only 90 degrees, 180 degrees, and 270 degrees
#     """
#     (h, w) = image.shape[:2]

#     # Get the rotation matrix for rotating and scaling the image
#     M = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)

#     # Compute the new bounding dimensions of the image
#     new_w = int(h * abs(np.sin(np.radians(angle))) + w * abs(np.cos(np.radians(angle))))
#     new_h = int(h * abs(np.cos(np.radians(angle))) + w * abs(np.sin(np.radians(angle))))

#     # Adjust the rotation matrix to account for the translation
#     M[0, 2] += (new_w - w) / 2
#     M[1, 2] += (new_h - h) / 2

#     # Perform the rotation
#     rotated = cv2.warpAffine(
#         image, M, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
#     )
#     return rotated


# cv2.rotate: for only 90 degree specific, but high performance
def rotate_image(image, angle):
    if angle == 90:
        print(f"rotate_image: {angle}:cv2.ROTATE_90_COUNTERCLOCKWISE")
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif angle == 180:
        print(f"rotate_image: {angle}:cv2.ROTATE_180")
        return cv2.rotate(image, cv2.ROTATE_180)
    elif angle == 270:
        print(f"rotate_image: {angle}:cv2.ROTATE_90_CLOCKWISE")
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    else:
        print(f"rotate_image: {angle}")
        return image


# cv2.warpAffine: any degree is possible, but low performance
# refer to: https://www.codevace.com/py-opencv-rotation/
def warpAffine_rotaion(src, angle, scale):
    """
    Rotates an image counterclockwise by the specified angle and returns a resized image to fit the rotated image size
    """
    # get size from input image
    height, width = src.shape[:2]
    # set center position for rotation
    center = (width // 2, height // 2)

    # 変換行列(回転行列)を計算
    M = cv2.getRotationMatrix2D(center, angle, scale)

    # 回転後の画像のサイズを計算
    cos_theta = np.abs(M[0, 0])
    sin_theta = np.abs(M[0, 1])
    new_width = int(width * cos_theta + height * sin_theta)
    new_height = int(width * sin_theta + height * cos_theta)

    # 回転の中心のズレを修正
    M[0, 2] += (new_width - width) / 2.0
    M[1, 2] += (new_height - height) / 2.0

    # 画像を反時計回りにangle°回転する
    return cv2.warpAffine(src, M, (new_width, new_height))


def remove_background(image):

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to the image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a mask from the contours
    mask = np.zeros_like(image)
    cv2.drawContours(mask, contours, -1, (255, 255, 255), thickness=cv2.FILLED)

    # Bitwise-and mask and original image
    return cv2.bitwise_and(image, mask)


# FIXME: It doesn't work yet
def deskew_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Use Canny edge detection to find edges
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and find the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    largest_contour = contours[0]

    # Approximate the contour to a polygon and find the bounding box
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    if len(approx) != 4:
        print(
            "The largest contour does not have 4 corners, deskewing may not be accurate."
        )
        return image

    # Get the coordinates of the four corners
    pts = np.float32([point[0] for point in approx])

    # Sort points to consistent order: top-left, top-right, bottom-right, bottom-left
    def order_points(pts):
        rect = np.zeros((4, 2), dtype="float32")
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        rect[0] = pts[np.argmin(s)]  # Top-left point will have the smallest sum
        rect[2] = pts[np.argmax(s)]  # Bottom-right point will have the largest sum
        rect[1] = pts[
            np.argmin(diff)
        ]  # Top-right point will have the smallest difference
        rect[3] = pts[
            np.argmax(diff)
        ]  # Bottom-left point will have the largest difference

        return rect

    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Calculate the width and height of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Define the destination points for the perspective transform
    dst = np.float32(
        [[0, 0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]]
    )

    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped
