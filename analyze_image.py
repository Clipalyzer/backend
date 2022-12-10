import cv2
import numpy as np
from PIL import Image
import pytesseract
from agents import agents
import re
from frame_positions import frame_positions

custom_oem_psm_config = r'--oem 3 --psm 6'
custom_oem_psm_config_numbers = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

def crop_image(img,obj):
    return img[obj["from"]["y"]:obj["to"]["y"], obj["from"]["x"]:obj["to"]["x"]]    

def find_text(img):
    return str(pytesseract.image_to_string(img, config=custom_oem_psm_config)).replace("\n","")

def find_numbers(img):
    text = str(pytesseract.image_to_string(img, config=custom_oem_psm_config_numbers)).replace("\n","")
    if text!="":
        return int(text)
    return -1

def print_progress(step,max,text):
    print("[{}{}] {}".format("#" * step," " * (15-step),text).ljust(max), end='\r')

def analyze_image(file):
    # print("{}".format("a" * 5))
    maxlen = len("[] Reading image {}".format(file)) + 15
    print_progress(1,maxlen,"Reading image {}".format(file))
    img = cv2.imread(file)
    print_progress(2,maxlen,"Read image")

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print_progress(3,maxlen,"grayed image")

    # Contrast scaling
    img2 = np.uint8(np.double(gray_img) + 80)
    positional_image = np.uint8(np.double(gray_img) + 120)
    money_image = np.uint8(np.double(gray_img) + 0)
    
    print_progress(4,maxlen,"calculated versions")

    image_data = {
        "file": file
    }

    image_data["time"] = find_text(crop_image(img2,frame_positions["time"]))
    print_progress(5,maxlen,"found time")
    if not re.search("[0-9]:[0-9][0-9]",image_data["time"]):
        image_data["time"]=""
    
    image_data["round_left"] = find_numbers(crop_image(img2,frame_positions["round_left"]))
    print_progress(6,maxlen,"found round_left")
    
    image_data["round_right"] = find_numbers(crop_image(img2,frame_positions["round_right"]))
    print_progress(7,maxlen,"found round_right")
    
    image_data["buy_phase"] = re.match("BUY PHASE",find_text(crop_image(img2,frame_positions["buy_phase"]))) != None
    # image_data["buy_phase1"] = find_text(crop_image(img2,frame_positions["buy_phase"]))
    print_progress(8,maxlen,"found buy_phase")
    
    image_data["side"] = find_text(crop_image(positional_image,frame_positions["side"]))
    print_progress(9,maxlen,"found side")
    if image_data["side"] != "DEFENDERS" and image_data["side"] != "ATTACKERS":
        image_data["side"] = ""

    image_data["hp"] = find_numbers(crop_image(positional_image,frame_positions["hp"]))
    print_progress(10,maxlen,"found hp")
    
    image_data["shield"] = find_numbers(crop_image(positional_image,frame_positions["shield"]))
    print_progress(11,maxlen,"found shield")
    
    image_data["money"] = find_numbers(crop_image(money_image,frame_positions["money"]))
    print_progress(12,maxlen,"found money")
    image_data["money"]=int(str(image_data["money"])[1:])
    
    image_data["spectating"] = find_text(crop_image(img2,frame_positions["spectating"]))
    print_progress(13,maxlen,"found spectating")
    if not image_data["spectating"] in agents:
        image_data["spectating"] = ""
    
    image_data["position"] = find_text(crop_image(positional_image,frame_positions["position"]))
    print_progress(14,maxlen,"found position")
    
    print_progress(15,maxlen,"done")
    
    return image_data
