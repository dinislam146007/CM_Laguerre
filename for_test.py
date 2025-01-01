import cv2
import numpy as np
import os

from PIL import Image
import requests


def extract_candle_colors(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV for better color detection
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges for red, orange, green, and gray candles
    color_ranges = {
        "red": [(0, 50, 50), (10, 255, 255)],
        "orange": [(11, 50, 50), (25, 255, 255)],
        "green": [(50, 50, 50), (90, 255, 255)],
        "gray": [(0, 0, 50), (180, 50, 200)],
    }

    # Create a list to store detected colors for each candle
    detected_candles = []

    # Loop through each color range and detect colors in the image
    masks = {}
    for color_name, (lower, upper) in color_ranges.items():
        # Convert the color range to numpy arrays
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)

        # Create a mask for the current color
        masks[color_name] = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Combine masks to find contours of candles
    combined_mask = sum(masks.values())
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Calculate the bounding box of the contour
        x, y, w, h = cv2.boundingRect(contour)
        if h > 10 and w > 5:  # Filter out small or irrelevant contours
            candle_colors = []
            for color_name, mask in masks.items():
                # Check if the current color is present in the candle area
                candle_region = mask[y:y+h, x:x+w]
                if cv2.countNonZero(candle_region) > 0:
                    candle_colors.append(color_name)

            # Sort colors by predefined priority: red > orange > green > gray
            priority = {"red": 1, "orange": 2, "green": 3, "gray": 4}
            candle_colors.sort(key=lambda color: priority[color])

            # Combine colors into a single entry per candle
            if len(candle_colors) > 1:
                detected_candles.append(f"[{', '.join(candle_colors)}]")
            else:
                detected_candles.append(candle_colors[0])

    return detected_candles

# Usage example
image_path = "image.jpeg"
# candle_colors = extract_candle_colors(image_path)
# print(candle_colors)
im = Image.open("image.jpeg")
print(im.load())