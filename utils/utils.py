import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import os


def convert_ratio_coordinate(coordinate_list, image=None, coord=()):
    x1, y1, delta_x, delta_y = coordinate_list
    if image is not None:
        Y = image.shape[0]
        X = image.shape[1]
        print("H-W-auto",(Y,X))
    else:
        X = coord[0]
        Y = coord[1]
        print("H-W-auto",(Y,X))
    ratio_x = x1/X
    ratio_y = y1/Y
    ratio_delta_x = delta_x / X
    ratio_delta_y = delta_y / Y
    return ratio_x, ratio_y, ratio_delta_x, ratio_delta_y


def convert_delta(coordinate_list):
    x1, y1, x2, y2 = coordinate_list
    delta_x = abs(x2 - x1)
    delta_y = abs(y2 - y1)
    return (x1, y1, delta_x, delta_y)


def convert_delta_to_absolute(coordinate) -> object:
    x1, y1, delta_x, delta_y = coordinate
    x2, y2 = x1 + delta_x, y1 + delta_y
    return (x1, y1, x2, y2)


def convert_ratio_to_abs(img,coordinate_def):
    x = math.ceil(img.shape[1]*coordinate_def[0])
    y = math.ceil(img.shape[0]*coordinate_def[1])
    delta_x = math.ceil(img.shape[1]*coordinate_def[2])
    delta_y = math.ceil(img.shape[0]*coordinate_def[3])
    x1 = x
    x2 = x + delta_x
    y1 = y
    y2 = y + delta_y
    return x1, y1, x2, y2


def draw_reg(path_img, coordinate_elim):
    img = cv2.imread(path_img)
    color = [0,0,255]
    thickness = 3
    x1, y1, x2, y2 = convert_ratio_to_abs(img, coordinate_elim)
    image = cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    plt.imshow(image)
    plt.show()


def load_coord_txt(path):
    dict_coord = dict()
    key_name = ["frame_size", "lines_text"]
    with open(os.path.split(path)[0] + '/' + 'coord.txt','r') as fh:
        for line, key in zip(fh, key_name):
            line = line.strip()
            dict_coord[key] = line
            # x,y,delta_x, delta_y = line.split(",")
            # return (int(x),int(y),int(delta_x), int(delta_y))
    print(dict_coord["frame_size"])
    w,h = dict_coord["frame_size"].split(",")
    x, y, delta_x, delta_y = dict_coord["lines_text"].split(",")
    return (int(w), int(h), int(x), int(y) ,int(delta_x), int(delta_y))


def get_relative_coord_one_times(full_path, EVENT_TYPE, save_txt=False):
    get_delta = load_coord_txt(full_path)[2:]
    w, h = load_coord_txt(full_path)[:2]
    frame_size = (w, h)
    coordinate_elim = convert_ratio_coordinate(get_delta, image=None, coord=frame_size)
    # my_var_name = [ k for k,v in locals().items() if v == EVENT_TYPE][0]
    my_var_name = EVENT_TYPE
    print("{} {}".format(my_var_name,coordinate_elim))
    coordinate_elim_str = [str(i) for i in coordinate_elim]
    coordinate_elim_str = ",".join(list(coordinate_elim_str))
    if save_txt:
        with open("{}".format("target_folder/coordinate_relative.txt"), "w") as f:
            f.write(coordinate_elim_str)
    return (my_var_name,coordinate_elim)


def check_bound_box_images(path, EVENT_TYPE):

    list_img = [i for i in os.listdir(path) if i.endswith(".jpg") or i.endswith(".JPG")]
    for img in list_img:
        print(img)
        full = path + "/" + img
        get_delta = load_coord_txt(full)[2:]
        w,h = load_coord_txt(full)[:2]
        frame_size = (w,h)
        print("wid, height",(w,h))
        try:
            open(full, 'rb').close()
        except IOError:
            raise IOError("problem with input file")
        image = cv2.imread(full)
        coordinate_elim = convert_ratio_coordinate(get_delta, image=None, coord=frame_size)
        # my_var_name = [k for k, v in locals().items() if v == EVENT_TYPE][0]
        my_var_name = EVENT_TYPE
        print("{} {}".format(my_var_name, coordinate_elim))
        draw_reg(full, coordinate_elim)


class WriteRead:
    def __init__(self, source_folder, target_folder, filename):
        self.source_folder = source_folder
        self.target_folder = target_folder
        self.filename = filename
        self.full_path = os.path.join(self.target_folder, self.filename)

    def write_file(self, message):
        with open("{}".format(self.full_path), "w") as f:
            f.write(json.dumps(message))

    def read_file(self):
        with open("{}".format(self.full_path), "r") as f:
            content = f.read()
            content = content.strip()
            list_content = content.split(",")
        list_content = [float(i) for i in list_content]
        return list_content













# path = "C:/Users/DELL/Downloads/super_smart_pro"
# path = "C:/Users/DELL/Downloads/nba2k23/label_doc"
# full_path =  path + "/" + "coord.txt"
# frame_size = (1224,686)
# EVENT_TYPE = "GAME"
# my_var_name,coordinate_elim = get_relative_coord_one_times(full_path, EVENT_TYPE)
# check_bound_box_images(path, EVENT_TYPE)



# Manual Test
# get_delta = convert_delta(EVENT_TYPE)
# # coordinate_elim = convert_ratio_coordinate(get_delta, image=None, coord=coord)
# # my_var_name = [ k for k,v in locals().items() if v == EVENT_TYPE][0]
# # print("{} {}".format(my_var_name,coordinate_elim))
#
#
#
# list_img = [i for i in os.listdir(path) if i.endswith(".jpg") or i.endswith(".JPG")]
# # list_img = ["new_ui.JPG"]
# for img in list_img:
#     print(img)
#     full = path + "/" + img
#     load_coord_txt(full)
#     break
#     # try:
#     #     open(full, 'rb').close()
#     # except IOError:
#     #     raise IOError("problem with input file")
#     # image = cv2.imread(full)
#     # coordinate_elim = convert_ratio_coordinate(get_delta, image=None, coord=coord)
#     # my_var_name = [k for k, v in locals().items() if v == EVENT_TYPE][0]
#     # print("{} {}".format(my_var_name, coordinate_elim))
#     # draw_reg(full, coordinate_elim)




