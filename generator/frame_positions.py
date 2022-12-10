frame_positions = {
    "time": {"from": {"x": 924, "y": 30}, "to": {"x": 994, "y": 67}},
    "round_left": {"from": {"x": 808, "y": 30}, "to": {"x": 838, "y": 67}},
    "round_right": {"from": {"x": 1080, "y": 30}, "to": {"x": 1115, "y": 67}},
    "buy_phase": {"from": {"x": 830, "y": 168}, "to": {"x": 1092, "y": 234}},
    "side": {"from": {"x": 969, "y": 145}, "to": {"x": 1075, "y": 165}},
    "position": {"from": {"x": 200, "y": 20}, "to": {"x": 300, "y": 40}},
    "hp": {"from": {"x": 578, "y": 1006}, "to": {"x": 648, "y": 1046}},
    "shield": {"from": {"x": 542, "y": 1014}, "to": {"x": 568, "y": 1038}},
    "money": {"from": {"x": 1790, "y": 1034}, "to": {"x": 1872, "y": 1056}},
    "spectating": {"from": {"x": 116, "y": 825}, "to": {"x": 205, "y": 851}},
    "map": {"from": {"x": 40, "y": 20}, "to": {"x": 500, "y": 480}},
}


def sub_list_from_frame_position(lst, name):
    temp = frame_positions[name]
    return lst[temp["from"]["x"] : temp["to"]["x"], temp["from"]["y"] : temp["to"]["y"]]
