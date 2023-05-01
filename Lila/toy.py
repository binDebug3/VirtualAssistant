import pyautogui
import numpy as np
import time
import cv2


def find_blank_space():
    return cv2.boundingRect(
        max(cv2.findContours(
            cv2.bitwise_not(
                cv2.dilate(
                    cv2.Canny(
                        np.mean(
                            np.array(
                                pyautogui.screenshot()      # Take a screenshot
                            ),                              # Convert the screenshot to a numpy array
                            axis=2),                        # Convert the screenshot to grayscale
                        50, 150),                           # Find the edges of the non-blank areas using Canny
                    np.ones((10, 10), np.uint8),            # Create a 10x10 matrix of 1s as a kernel for dilation
                    iterations=1)                           # Dilate edges to make the non-blank areas larger
            ),                                              # Invert the dilated part to make a mask of blank
            cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0],     # Find the contours of the blank areas in the mask
            key=cv2.contourArea)                            # Find the largest contour (the blank area)
    )                                                       # Get the bounding rectangle of the largest contour


def get_center(x, y, w, h):
    return x + w // 2, y + h // 2


def detect_change(threshold=30):
    # Take the first screenshot
    previous_screenshot = pyautogui.screenshot()

    while True:
        # Take the current screenshot
        time.sleep(10)
        current_screenshot = pyautogui.screenshot()

        # Calculate the mean pixel value of the difference array
        mean_difference = np.mean(
            np.mean(
                np.abs(
                    np.array(current_screenshot) - np.array(previous_screenshot)
                ),
                axis=2)
        )

        if mean_difference > threshold:
            yield get_center(find_blank_space())

        # Set the current screenshot as the previous screenshot for the next iteration
        previous_screenshot = current_screenshot
