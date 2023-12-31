import numpy as np



IMG_SCALE_GOAL = 0.7
IMG_SCALE = 1.2
GRAY_THRESH_LOW = 100
GRAY_THRESH_HIGH = 255



# coordinate of crop region y1,y2,x1,x2

red_card_coordinate = (110,132,218,298)
yellow_card_coordinate = (129,149,189,308)
# goal_coordinate = (600,640,600,675)
goal_coordinate = (569,640,605,675)


# color filter

RED_IMG_SCALE_COLOR = 1.2
RED_THRESH_COLOR_LOW = 100
RED_THRESH_COLOR_HIGH = 255

YELLOW_IMG_SCALE_COLOR = 1.2
YELLOW_THRESH_COLOR_LOW = 100
YELLOW_THRESH_COLOR_HIGH = 255

GOAL_IMG_SCALE_COLOR = 1.2
GOAL_THRESH_COLOR_LOW = 100
GOAL_THRESH_COLOR_HIGH = 255



THRESHOLD_COLOR_RED_CARD = 1000
THRESHOLD_COLOR_YELLOW_CARD = 1000
THRESHOLD_COLOR_GOAL_CARD = 50


# Dark blue goal
LOWER_RANGE_DARK = np.array([47, 33, 24])
UPPER_RANGE_DARK = np.array([56, 44, 44])
# Light Blue goal
LOWER_RANGE_LIGHT = np.array([113, 33, 24])
UPPER_RANGE_LIGHT = np.array([151, 59, 37])

LOWER_RANGE_PURPLE = np.array([21, 0, 37])
UPPER_RANGE_PURPLE = np.array([31, 0, 64])
