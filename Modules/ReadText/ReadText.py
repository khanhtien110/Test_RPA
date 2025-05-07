from paddleocr import PaddleOCR
import pytesseract
from PIL import Image
import numpy as np
import cv2
class RPAReadText:
    def read_Img_PaddleOCR(self, path_img, lang="en"):
        if not path_img:
            return -1
        else:
            try:
                ocr = PaddleOCR(use_angle_cls=True, lang=lang)  
                image_path = path_img
                result = ocr.ocr(image_path, cls=False)

                for line in result:
                    for word_info in line:
                        text = word_info[1][0]
                        return text
            except Exception as e:
                return e
    def read_Img_Pytesseract(self, path_img, is_high_complexity=False, is_Line_or_shapes=False):
        if not path_img:
            return -1
        else:
            try:
                image = Image.open(path_img)
                if is_high_complexity:
                    image = np.array(image)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (5,5), 0)
                    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                    kernel = np.ones((3,3), np.uint8)
                    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                    dilated = cv2.dilate(cleaned, kernel, iterations=1)
                    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                    text = pytesseract.image_to_string(dilated, config=custom_config)
                    return text
                else:
                    text = pytesseract.image_to_string(image)
                    return text
            except Exception as e:
                return e
    def read_Img_CV2(self, path_img, is_high_complexity=False):
        if not path_img:
            return -1
        else:
            try:
                image = cv2.imread(path_img)
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                kernel = np.ones((3,3), np.uint8)
                cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
                custom_config = r'--oem 3 --psm 6' 
                if is_high_complexity:
                    dilated = cv2.dilate(thresh, kernel, iterations=1)
                    text = pytesseract.image_to_string(dilated, config=custom_config)
                    return text

                text = pytesseract.image_to_string(cleaned, config=custom_config)
                return text
            except Exception as e:
                return e
