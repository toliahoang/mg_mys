# goal_pattern = "\d{1,2}[\p{Han}!-\/:-@[-`{-~ ]\d{1,2}"
goal_pattern = "\d{1,2}[^[^0-9]*$]\d{1,2}"
red_card_pattern = "(?i)RED"
yellow_card_pattern = "(?i)YELLOW"
from re import match
import re
# print("img {} text_easyocr_readtext {}".format(i, result_easyocr_readtext))

def get_match_str(pos_pattern_list, neg_pattern_list,text):
    pos_value = []
    for pos_parse in pos_pattern_list:
        pos_value += list(filter(lambda v: match(pos_parse, v), [text]))
    neg_value = []
    for neg_parse in neg_pattern_list:
        neg_value += list(filter(lambda v: match(neg_parse, v), [text]))
    if pos_value and not neg_value:
        return True
    else:
        return False


def get_match_data(pos_pattern_list, neg_pattern_list , text_list):
    pos_values = []
    for pos_parse in pos_pattern_list:
        pos_values += list(filter(lambda v: match(pos_parse, v), text_list))
    neg_values = []
    for neg_parse in neg_pattern_list:
        neg_values += list(filter(lambda v: match(neg_parse, v), text_list))
    if pos_values and not neg_values:
        return True
    return False

def get_match_data_easyocr(pos_pattern_list, neg_pattern_list , text_list):
    pos_values = []
    for pos_parse in pos_pattern_list:
        pos_values += list(filter(lambda v: match(pos_parse, v, re.IGNORECASE), text_list))
    neg_values = []
    for neg_parse in neg_pattern_list:
        neg_values += list(filter(lambda v: match(neg_parse, v, re.IGNORECASE), text_list))
    if pos_values and not neg_values:
        return True
    return False


def get_match_str_easyocr(pos_pattern_list, neg_pattern_list , text_list):
    pos_values = []
    for pos_parse in pos_pattern_list:
        pos_values += list(filter(lambda v: match(pos_parse, v, re.IGNORECASE), text_list))
    neg_values = []
    for neg_parse in neg_pattern_list:
        neg_values += list(filter(lambda v: match(neg_parse, v, re.IGNORECASE), text_list))
    if pos_values and not neg_values:
        return True
    return False


def get_match_general(pos_pattern_list, neg_pattern_list ,text, mode):

    if mode == 'img2data':
        return get_match_data(pos_pattern_list, neg_pattern_list,text)
    if mode == 'img2str':
        return get_match_str(pos_pattern_list, neg_pattern_list,text)
    if mode == 'img2data_easyocr':
        print("mode img2data_easyocr")
        return get_match_data_easyocr(pos_pattern_list, neg_pattern_list, text)
    if mode == 'img2str_easyocr':
        print("mode img2str_easyocr")
        return get_match_str_easyocr(pos_pattern_list, neg_pattern_list, text)
# params = {'white_list':["\d{1,2}[!-\/:-@[-`{-~ ]\d{1,2}", "\d{1,2}[^0-9]\d{1,2}"], 'black_list': ["[0][!-\/:-@[-`{-~ ][0]", "[0][^0-9][0]"], 'mode':'img2data_easyocr'}
# match = get_match_general(params['white_list'], params['black_list'],['1-0'], mode = params['mode'])
# print("match_status:", match)



