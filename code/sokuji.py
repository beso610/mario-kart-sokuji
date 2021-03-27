import os
import sys
import pyocr, pyocr.builders
import numpy as np
from PIL import Image

def setup_path():
    path = "C:\\Program Files\\Tesseract-OCR" # Tesseractのパス
    path_list = os.environ["PATH"].split(os.pathsep)
    if path not in path_list:
        os.environ["PATH"] += os.pathsep + path

def optimize(image):
    border = 158
    arr = np.array(image)
    """
    print(arr.ndim)
    print(arr.shape)
    print(arr.size)
    """
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
            if pix[0] < border or pix[1] < border or pix[2] < border: # 暗めの色は白に
                arr[i][j] = [255, 255, 255]
            elif pix[0] >= border or pix[1] >= border or pix[2] >= border: # 白文字は黒に
                arr[i][j] = [0, 0, 0]
    return Image.fromarray(arr)

def recognize(image, lang):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool")
        sys.exit(1)

    text = tools[0].image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=7))
    print(text)

def get_name():
    START_X_NAME = 1010
    START_Y_NAME = 77
    WIDTH_NAME = 426
    HEIGHT_NAME = 70

    START_X_SCORE = 1680
    #START_X_SCORE = 1750
    START_Y_SCORE = 77
    WIDTH_SCORE = 160
    #WIDTH_SCORE = 90
    HEIGHT_SCORE = 70

    GAP = 8

    image = Image.open("..\data\\test\mk_test3.jpg")
    x, y = START_X_NAME, START_Y_NAME
    s, t = START_X_SCORE, START_Y_SCORE
    names = []
    scores = []
    for i in range(12):
        names.append(image.crop((x, y, x+WIDTH_NAME, y+HEIGHT_NAME)))
        y += HEIGHT_NAME + GAP

    for i in range(12):
        scores.append(image.crop((s, t, s+WIDTH_SCORE, t+HEIGHT_SCORE)))
        t += HEIGHT_SCORE + GAP

    for i in range(len(names)):
        optimize(names[i]).save('..\data\\name\\name{}.jpg'.format(i))
        optimize(scores[i]).save('..\data\score\score{}.jpg'.format(i))
        recognize(optimize(names[i]), 'jpn')
        recognize(optimize(scores[i]), 'letsgodigital')


if __name__ == "__main__":
    setup_path()
    get_name()

