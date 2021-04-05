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

def separate_name():
    START_X_NAME = 1010
    START_Y_NAME = 77
    WIDTH_NAME = 426
    HEIGHT_NAME = 70
    GAP = 8

    image = Image.open("mk_test.jpg")
    x, y = START_X_NAME, START_Y_NAME
    names = []

    for i in range(12):
        names.append(image.crop((x, y, x+WIDTH_NAME, y+HEIGHT_NAME)))
        y += HEIGHT_NAME + GAP

    return names

def analysis_name(names_image):
    names_extract = []
    for i in range(len(names_image)):
        name_optimized = optimize(names_image[i])
        #name_optimized.save('name{}.jpg'.format(i))
        names_extract.append(recognize(name_optimized, 'jpn'))

    return names_extract

def separate_score():
    START_X_SCORE = 1696
    START_Y_SCORE = 77
    WIDTH_SCORE = 130
    HEIGHT_SCORE = 70
    GAP = 8
    SPLIT = 26
    image = Image.open("mk_test3.jpg")
    #image = Image.open('mk_test4.png').convert('RGB').save('mk_test4.jpg')
    t = START_Y_SCORE
    scores = []
    for i in range(12):
        s = START_X_SCORE
        score_digit = []
        for j in range(5):
            score_digit.append(image.crop((s, t, s+SPLIT, t+HEIGHT_SCORE)))
            s += SPLIT
        scores.append(score_digit)
        t += HEIGHT_SCORE + GAP

    return scores

def analysis_score(scores_image):
    scores_extract = []
    for i in range(len(scores_image)):
        scores_tmp = []
        for j in range(5):
            score_optimized = optimize(scores_image[i][j])
            score_optimized.save('score{}{}.jpg'.format(i, j))
            scores_tmp.append(score_optimized)
        #scores_extract.append(recognize(score_optimized, 'letsgodigital'))
        scores_extract.append(calculate_score(scores_tmp))

    return scores_extract

def calculate_score(scores):
    scores_img = scores
    digit = len(scores_img)
    score = 0
    for i, l in enumerate(scores_img):
        num = check_number(l)
        score += num * 10**(digit-i-1)
    print(score)
    return score

def check_number(img):
    arr = np.array(img)
    dig = [0 for i in range(7)]

    if len(arr) < 30:
        return 0

    if all(arr[2][12] == [0, 0, 0]):
        dig[0] = 1
    if all(arr[9][20] == [0, 0, 0]):
        dig[1] = 1
    if all(arr[23][20] == [0, 0, 0]):
        dig[2] = 1
    if all(arr[30][12] == [0, 0, 0]):
        dig[3] = 1
    if all(arr[23][4] == [0, 0, 0]):
        dig[4] = 1
    if all(arr[9][4] == [0, 0, 0]):
        dig[5] = 1
    if all(arr[16][12] == [0, 0, 0]):
        dig[6] = 1

    num = pattern_match_number(dig)
    return num


def pattern_match_number(dig):
    if dig == [1, 1, 1, 1, 1, 1, 0]:
        return 0
    elif dig == [1, 1, 0, 1, 1, 0, 1]:
        return 2
    elif dig == [1, 1, 1, 1, 0, 0, 1]:
        return 3
    elif dig == [0, 1, 1, 0, 0, 1, 1]:
        return 4
    elif dig == [1, 0, 1, 1, 0, 1, 1]:
        return 5
    elif dig == [1, 0, 1, 1, 1, 1, 1]:
        return 6
    elif dig == [1, 1, 1, 0, 0, 0, 0]:
        return 7
    elif dig == [1, 1, 1, 1, 1, 1, 1]:
        return 8
    elif dig == [1, 1, 1, 1, 0, 1, 1]:
        return 9
    else:
        return 1

def optimize(image):
    border = 158
    start = -1
    arr = np.array(image)
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

    arr_rm_upper = arr[start:]
    return Image.fromarray(arr_rm_upper)


def recognize(image, lang):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool")
        sys.exit(1)

    text = tools[0].image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=7))

    return text


if __name__ == "__main__":
    setup_path()
    #names_image = separate_name()
    scores_image = separate_score()
    #names_extract = analysis_name(names_image)
    scores_extract = analysis_score(scores_image)

