import sys
import pyautogui
import psutil
import pywinctl
import win32gui
import win32process
import time
import os
import shutil
import cv2
import numpy as np
from Modules.Utils import utils


class RPACapture:
    _instance = None

    def __new__(cls, *args, **kwargs):
        # If no instance exists, create it
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_data, rpa_tracker):
        self.config_data = config_data
        self.rpa_tracker = rpa_tracker
        self.screenshot_1_dir = (
            self.config_data["screenshot_1_dir"]
            if not utils.is_null_or_empty(self.config_data["screenshot_1_dir"])
            else "C:\\RPA\\Screenshot_1"
        )
        self.screenshot_2_dir = (
            self.config_data["screenshot_2_dir"]
            if not utils.is_null_or_empty(self.config_data["screenshot_2_dir"])
            else "C:\\RPA\\Screenshot_2"
        )
        self.screenshot_temp_dir = (
            self.config_data["screenshot_temp_dir"]
            if not utils.is_null_or_empty(self.config_data["screenshot_temp_dir"])
            else "C:\\RPA\\Screenshot_Temp"
        )

        self.screenshot_1_img = ""

    def capture_window(self, pid, file_name):
        window = self.get_window_by_pid(pid)
        if window:
            window.maximize()
            window.activate()  # Bring the window to the front
            time.sleep(1)  # Give it a second to focus
            screenshot = pyautogui.screenshot(
                region=(window.left, window.top, window.width, window.height)
            )

            if utils.is_null_or_empty(file_name):
                file_name = "screenshot_temp.png"

            self.clear_folder(self.screenshot_temp_dir)
            screenshot.save(self.screenshot_temp_dir + "\\" + file_name)
            window.minimize()

            self.detect_image_and_crop(self.screenshot_temp_dir + "\\" + file_name)

        else:
            print("Not found any process with PID: " + pid)

    def get_window_by_pid(self, pid):
        for window in pywinctl.getAllWindows():
            hwnd = window._hWnd  # Get the native window handle
            _, window_pid = win32process.GetWindowThreadProcessId(
                hwnd
            )  # Get PID from handle
            if window_pid == pid:
                return window
        return None

    def clear_folder(self, folder_path):

        if os.path.exists(folder_path):
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)  # Remove file
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)  # Remove folder and its contents
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        else:
            os.makedirs(folder_path, exist_ok=True)

    def save_images(self):
        self.clear_folder(self.screenshot_2_dir)

        for file_name in os.listdir(self.screenshot_1_dir):
            source_path = os.path.join(self.screenshot_1_dir, file_name)
            destination_path = os.path.join(self.screenshot_2_dir, file_name)
        self.clear_folder(self.screenshot_2_dir)
        self.clear_folder(self.screenshot_temp_dir)
        self.screenshot_1_img = ""

    def detect_image_and_crop(self, file_name):
        # Load the image
        image = cv2.imread(filename=file_name)

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for yellow color in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask for yellow color
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (assuming the yellow square is the largest)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)

            # Get bounding box (x, y, width, height)
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Crop the detected area
            cropped_image = image[y : y + h, x : x + w]

            # # Show cropped image
            # cv2.imshow("Cropped Yellow Area", cropped_image)
            # time.sleep(0.5)
            # # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            self.clear_folder(self.screenshot_1_dir)
            # Save the cropped image
            cv2.imwrite(
                self.screenshot_1_dir + "\\" + "screenshot_1.png",
                cropped_image,
            )
            self.screenshot_1_img = self.screenshot_1_dir + "\\" + "screenshot_1.png"
        else:
            print("No yellow square detected.")
            self.screenshot_1_img = ""

    def send_data(self, type = 1):
        pass


