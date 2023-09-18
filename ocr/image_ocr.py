import cv2
import numpy as np
import matplotlib.pyplot as plt
from config.common import *
import re
import os
from re import match
from sklearn import metrics
import math
import numpy as np
import easyocr
reader = easyocr.Reader(['en']) # this needs to run only once to load the model into memory
import matplotlib.pyplot as plt
from config.regex_config import *


class OcrPrepocessing():

    def __init__(self, frame):
        self.frame = frame

    def color_filter(self, img_scale,gray_thresh_low, gray_thresh_high, event):
        img = cv2.resize(self.frame, None, fx=img_scale, fy=img_scale, interpolation=cv2.INTER_CUBIC)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if event == "red_card":
            _,gray = cv2.threshold(gray, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
            sum_white_pixel = np.sum(gray == 255)
            return sum_white_pixel

        if event == "yellow_card":
            _,gray = cv2.threshold(gray, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
            sum_white_pixel = np.sum(gray == 255)
            return sum_white_pixel

        if event == "goal":
            _,gray = cv2.threshold(gray, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
            sum_white_pixel = np.sum(gray == 255)
            return sum_white_pixel

    def color_filter_specific(self,frame, lower_range_dark, upper_range_dark):
        mask_color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        white_mask = cv2.inRange(mask_color,np.array(lower_range_dark), np.array(upper_range_dark))
        res = cv2.bitwise_and(frame,frame , mask=white_mask)
        # cv2.imshow("res ",white_mask)
        # cv2.waitKey(0)
        sum_white_pixel_dark = np.sum(white_mask == 255)
        sorted_white_pixel = sorted([sum_white_pixel_dark], reverse=True)
        for i in sorted_white_pixel:
            if i > 0:
                return i
            else:
                return 0

    def color_filter_specific_range(self, frame, color_range):
        if len(color_range) == 0:
            return 0
        sum_white_pixel_dark = []
        for color in color_range:
            mask_color = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            white_mask = cv2.inRange(mask_color, np.array(color[0]), np.array(color[1]))
            sum_white_pixel_dark.append(np.sum(white_mask == 255))
        sorted_white_pixel = sorted(sum_white_pixel_dark, reverse=True)
        for i in sorted_white_pixel:
            if i > 0:
                return i
            else:
                return 0

    def image_process_img2data(self, frame ,img_scale, gray_thresh_low, gray_thresh_high):
        img = cv2.resize(frame, None, fx=img_scale, fy=img_scale, interpolation=cv2.INTER_CUBIC)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # _,rgb = cv2.threshold(rgb, gray_thresh_low, gray_thresh_high, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
        _,rgb = cv2.threshold(rgb, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
        # cv2.imshow("img", rgb)
        # cv2.waitKey(0)
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
        return results

    def image_process_img2data_test(self, frame, img_scale, gray_thresh_low, gray_thresh_high, lower_range_dark, upper_range_dark):

        frame = self.skew_correction(frame, 6)

        img = cv2.resize(frame, None, fx=img_scale, fy=img_scale, interpolation=cv2.INTER_CUBIC)
        mask_color = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        white_mask = cv2.inRange(mask_color,lower_range_dark, upper_range_dark)
        white_mask = 255 - white_mask
        res = cv2.bitwise_and(img,img , mask=white_mask)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,rgb = cv2.threshold(rgb, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
        kernel = np.ones((6, 6), np.uint8)
        rgb = cv2.dilate(rgb, kernel, iterations=2)
        # plt.imshow(rgb)
        # plt.show()
        results = pytesseract.image_to_data(rgb, output_type=Output.DICT)
        return results

    def skew_correction(self, img, angle, skew_status = None):
        # rotate the image to deskew it
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def affine_transform(self, img, affine_ratio):
        rows, cols = img.shape[:2]
        src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1]])
        dst_points = np.float32([[0, 0], [int(1.0 * (cols - 1)), 0], [int(affine_ratio * (cols - 1)), rows - 1]])
        affine_matrix = cv2.getAffineTransform(src_points, dst_points)
        img_output = cv2.warpAffine(img, affine_matrix, (cols, rows))
        return img_output

    def image_process_img2str(self, frame, img_scale, gray_thresh_low, gray_thresh_high):
        img = cv2.resize(frame, None, fx=img_scale, fy=img_scale, interpolation=cv2.INTER_CUBIC)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _,rgb = cv2.threshold(rgb, gray_thresh_low, gray_thresh_high, cv2.THRESH_BINARY_INV)
        results = pytesseract.image_to_string(rgb, config='--psm 7',output_type=Output.DICT)
        return results

    def find_text_line(self):
        blurred = cv2.blur(self.frame, (3, 3))
        canny = cv2.Canny(blurred, 50, 150)
        bin_width = 15
        kernel = np.ones((5, 5), np.uint8)
        dilation = cv2.dilate(canny, kernel, iterations=1)
        x_hist = np.sum(dilation, axis=0)
        bin_values = self.discretize(x_hist, bin_width=bin_width)
        chunk = self.find_longest_segment(bin_values)
        x1 = chunk[0] * bin_width
        x2 = x1 + bin_width * (len(chunk) + 2)
        return x1, x2

    def discretize(self, array, bin_width):
        n_bin = int(len(array) / bin_width)
        bin_values = []
        for i in range(n_bin):
            end = i * bin_width + bin_width
            if end >= len(array):
                end = len(array)
            bin_value = sum(array[i * bin_width: end]) / (end - i * bin_width)
            bin_values.append(bin_value)
        return bin_values

    def find_longest_segment(self, array):
        print(array)
        segments = []
        current_segment = []
        for i, value in enumerate(array):
            if value > 0:
                current_segment.append(i)
            else:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []
        segments = sorted(segments, key=lambda x: len(x), reverse=True)
        return segments[0]


def color_filter_specific(frame, color_range, event):
    if len(color_range) == 0:
        return 0
    sum_white_pixel = []
    for color in color_range:
        color = list(color.values())[0]
        print("color",color)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        color_mask = cv2.inRange(frame_hsv, np.array(color[0]), np.array(color[1]))
        sum_white_pixel.append(np.sum(color_mask == 255))
    return sum_white_pixel


def convert_relative_to_absolute(img, coordinate_def):

        x = math.ceil(img.shape[1]*coordinate_def[0])
        y = math.ceil(img.shape[0]*coordinate_def[1])
        delta_x = math.ceil(img.shape[1]*coordinate_def[2])
        delta_y = math.ceil(img.shape[0]*coordinate_def[3])
        x1 = x
        x2 = x + delta_x
        y1 = y
        y2 = y + delta_y
        return x1, y1, x2, y2


def test_by_easyocr(path, coordinate_elim, params):

    list_img = [i for i in os.listdir(path) if i.endswith(".jpg") or i.endswith(".JPG")]
    white_score_list = []
    for i in list_img:
        full_path = path + "/" + i
        img = cv2.imread(full_path)
        x1, y1, x2, y2 = convert_relative_to_absolute(img, coordinate_elim)
        test_ocr = OcrPrepocessing(img[y1:y2,x1:x2])
        LOWER_RANGE_WHITE, UPPER_RANGE_WHITE = [0,0,200],[255,255,255]
        range_color = [[[0,0,200],[255,255,255]], [[188, 38, 97], [193,45,75]], [[151.09999999999994, 0, 61.0], [182.37037037037035, 62.72277227722772, 174.0]]]
        img = img[y1:y2,x1:x2]
        get_sum = color_filter_specific(img, [{"white_color": [[0, 0, 200], [255, 255, 255]]}], event=None)
        print("getsum",get_sum)
        get_status = test_ocr.color_filter_specific(img, LOWER_RANGE_WHITE,UPPER_RANGE_WHITE)
        height = img.shape[0]
        width = img.shape[1]
        new_width = width // 1
        ratio = new_width / width  # (or new_height / height)
        new_height = int(height * ratio)
        dimensions = (new_width, new_height)
        new_image = cv2.resize(img, dimensions, interpolation=cv2.INTER_CUBIC)
        plt.imshow(new_image)
        plt.show()
        result_easyocr_readtext = reader.readtext(new_image,detail = 0, mag_ratio=2)
        result_easyocr_recognize = reader.recognize(new_image, detail= 0)
        # print("img {} text_tesseract {}".format(i,result_tesseract['text']))
        print("img {} text_easyocr_readtext {}".format(i,result_easyocr_readtext))
        print("img {} text_easyocr_recognize {}".format(i,result_easyocr_recognize))
        print("img {} color_val {}".format(i, get_status))
        # params = {'white_list':["\d{1,2}[!-\/:-@[-`{-~ ]\d{1,2}", "\d{1,2}[^0-9]\d{1,2}"], 'black_list': ["0[!-\/:-@[-`{-~ ]\/0", "^.*(?i)TIME.*$"], 'mode':'img2data_easyocr'}
        # params = {'white_list':["^.*(?i)g[a-zA-Z]me.*$", "^.*(?i)tim smared.*$", "^.*(?i)tim snared.*$", "^.*(?i)blood collected.*$"], 'black_list': [], 'mode':'img2data_easyocr'}
        # match = get_match_general(params['white_list'], params['black_list'],result_easyocr_readtext, mode = params['mode'])
        params = params
        match = get_match_general(params['white_list'], params['black_list'],result_easyocr_readtext, mode = params['mode'])
        print("match_status:", match)
























