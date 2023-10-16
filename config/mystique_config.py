import json
import os
from utils.utils import WriteRead
access_dict = {"user":"user", "password":"pass", "host": "localhost", "database":"db"}
read_write = WriteRead(None, "target_folder", "coordinate_relative.txt")
content = read_write.read_file()









### Show database
game_dict = {"db":"streamscope", "table":"game", "id": "56"}
hyper_trigger_game_dict = {"db":"streamscope", "table":"hyper_trigger_game_config", "id": "55"}
select_sql = "SELECT * FROM {db}.{table} WHERE id={id};".format(**game_dict)







### config new game here ###
hyper_trigger_game_config_dict = {"id":56, "name":"'Forza Motorsport'",
                                  "description": "'Forza Motorsport'",
                                  "slug":"'forza-motorsport'", "category": "'forza-motorsport'",
                                  "seq_number":1000, "is_deleted": 0}
insert_game_sql = "INSERT INTO streamscope.game (id, name, description, slug, category, seq_number, is_deleted) VALUES ({id}, {name}, {description}, {slug}, {category}, {seq_number}, {is_deleted});".format(**hyper_trigger_game_config_dict)






### config new event here ###
get_txt = json.dumps({"list_ocr_thresh": [[2, 100, 255]],
                      "text_pos": content,
                      "img_color_scale": 1, "color_range": [{"high_white": [[0, 0, 200], [255, 255, 255]]}],
                      "color_pos": content,
                      "color_thresh": [-1], "white_list": ["^.*(?i)finished.*$"], "black_list": [],
                      "mode": "img2str_easyocr"})
event_dict = {"id": 102,
              "event_id": 700,
              "event_name": "'finished'",
              "game_id": 56,
              "config_params": get_txt
              }
insert_event_sql = "INSERT INTO streamscope.hyper_trigger_game_config (id, event_id, event_name, game_id, config_params) VALUES ({id}, {event_id}, {event_name}, {game_id}, '{config_params}');".format(**event_dict)

