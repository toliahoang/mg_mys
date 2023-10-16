from utils.get_coordinate_by_ui import draw_reg_get_coord
from utils.utils import check_bound_box_images, get_relative_coord_one_times
from ocr.image_ocr import test_by_easyocr
PATH = "C:/Users/ADMIN/Downloads/starfaire"


"""Draw to get Text coordinate"""
PATH_SINGLE_IMG = PATH + "/" + "mission_reward.JPG"
# draw_reg_get_coord(PATH_SINGLE_IMG)


"""Check Bounding Box"""
FULL_PATH =  PATH + "/" + "coord.txt"
EVENT_TYPE = "GAME"
# check_bound_box_images(PATH, EVENT_TYPE)




"""Test OCR"""
my_var_name,coordinate_elim = get_relative_coord_one_times(FULL_PATH, EVENT_TYPE, save_txt=True)
params = {'white_list': ["^.*(?i)g[a-zA-Z]me.*$", "^.*(?i)mission updated.*$", "^.*(?i)tim snared.*$",
                         "^.*(?i)blood collected.*$"], 'black_list': [], 'mode': 'img2str_easyocr'}

test_by_easyocr(PATH, coordinate_elim=coordinate_elim, params=params)
