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

def debug():
    image = Image.open("mk_test4.jpg")
    border = 158
    arr = np.array(image)
    start = -1
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
            if pix[0] < border or pix[1] < border or pix[2] < border: # 暗めの色は白に
                arr[i][j][0] = 255
                arr[i][j][1] = 255
                arr[i][j][2] = 255
            elif pix[0] >= border or pix[1] >= border or pix[2] >= border: # 白文字は黒に
                if start == -1:
                    start = i
                arr[i][j][0] = 0
                arr[i][j][1] = 0
                arr[i][j][2] = 0
    Image.fromarray(arr).save("debug.jpg")

if __name__ == "__main__":
    setup_path()
    debug()