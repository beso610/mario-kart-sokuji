import os
import sys
import pyocr, pyocr.builders
import numpy as np
from PIL import Image
from difflib import SequenceMatcher

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
    #path_in = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/test/Screenshot 2021-04-10 00-43-21.png')
    #path_in = 'D:マリオカート/Screenshot 2021-04-10 00-43-21.png'
    #image = Image.open(path_in)
    image = Image.open(sys.argv[-1])
    x, y = START_X_NAME, START_Y_NAME
    names = []

    for i in range(12):
        names.append(image.crop((x, y, x+WIDTH_NAME, y+HEIGHT_NAME)))
        y += HEIGHT_NAME + GAP

    return names

def analysis_name(names_image):
    names_extract = []
    path_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/name')
    for i in range(len(names_image)):
        name_optimized = optimize(names_image[i], 0)
        #name_optimized.save(path_out + '/name{}.jpg'.format(i))
        names_extract.append(recognize(name_optimized, 'jpn'))
    print(names_extract)
    return names_extract

def normalize_name(names_extract):
    return names_extract

def separate_score():
    START_X_SCORE = 1696
    START_Y_SCORE = 77
    WIDTH_SCORE = 130
    HEIGHT_SCORE = 70
    GAP = 8
    SPLIT = 26
    #path_in = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/test/Screenshot 2021-04-10 00-43-21.png')
    #path_in = 'D:マリオカート/Screenshot 2021-04-10 00-43-21.png'
    #image = Image.open(path_in)
    image = Image.open(sys.argv[-1])
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
    path_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/score')
    for i in range(len(scores_image)):
        scores_tmp = []
        for j in range(5):
            score_optimized = optimize(scores_image[i][j], 1)
            score_optimized.save(path_out + '/score{}{}.jpg'.format(i, j))
            scores_tmp.append(score_optimized)
        #scores_extract.append(recognize(score_optimized, 'letsgodigital'))
        scores_extract.append(calculate_score(scores_tmp))
    print(scores_extract)

    return scores_extract

def calculate_score(scores):
    scores_img = scores
    digit = len(scores_img)
    score = 0
    for i, l in enumerate(scores_img):
        num = check_number(l)
        score += num * 10**(digit-i-1)
    #print(score)
    return score

def check_number(img):
    arr = np.array(img)
    dig = [0 for i in range(7)]
    judge_one = 0

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
    if all(arr[7][12] == [0, 0, 0]):
        judge_one = 1

    num = pattern_match_number(dig, judge_one)
    return num


def pattern_match_number(dig, judge_one):
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
    elif judge_one == 1:
        return 1
    else:
        return 0

def optimize(image, type):
    arr = np.array(image)
    if (200 < arr[0][0][0]) and (200 < arr[0][0][1]):
        return optimize_me(arr, type)
    else:
        return optimize_other(arr, type)

def optimize_me(arr, type):
    border = 160
    start = -1
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            pix = arr[i][j]
            if (border < pix[0]) and (border < pix[1]): # 黄色は白に
                arr[i][j][0] = 255
                arr[i][j][1] = 255
                arr[i][j][2] = 255
            elif (border >= pix[0]) or (border >= pix[1]): # 黒文字は黒に
                if start == -1:
                    start = i
                arr[i][j][0] = 0
                arr[i][j][1] = 0
                arr[i][j][2] = 0

    if type == 1: #スコアのときは上の余白を削る
        arr_rm_upper = arr[start:]
        return Image.fromarray(arr_rm_upper)
    else: #名前の時は何もしない
        return Image.fromarray(arr)

def optimize_other(arr, type):
    border = 158
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

    if type == 1: #スコアのときは上の余白を削る
        arr_rm_upper = arr[start:]
        return Image.fromarray(arr_rm_upper)
    else: #名前の時は何もしない
        return Image.fromarray(arr)

def recognize(image, lang):
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool")
        sys.exit(1)

    text = tools[0].image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.TextBuilder(tesseract_layout=6))

    return text

def user_input():
    print("タグ名をスペース区切りで入力してください.")
    tags = list(map(str, input().split()))
    if (len(tags) != 2) and (len(tags) != 3) and (len(tags) != 4) and (len(tags) != 6):
        print("数が合いません. 正しく入力してください.")
        exit()
    return tags

def SequenceMatcher_append_zero(src, trg):
    s_len, t_len = len(src), len(trg)
    l = [SequenceMatcher(None, src, trg[i:i+s_len]).ratio() for i in range(t_len-s_len+1)]
    l.append(0)
    return l

def classify_name(tags, names_extract):
    classify_dict = dict()
    member_len = 12 // len(tags)
    choose_list = [0 for i in range(12)]
    for i in range(len(tags)):
        src = tags[i].upper()
        max_r = [0 for k in range(member_len)]
        max_index = [-1 for k in range(member_len)]
        for j in range(len(names_extract)):
            if choose_list[j] == 0:
                trg = names_extract[j].upper()
                s_len, t_len = len(src), len(trg)
                r = max(SequenceMatcher_append_zero(src, trg))
                for k in range(member_len):
                    if r > max_r[k]:
                        if k < (member_len - 1):
                            max_r[k+1] = max_r[k]
                            max_index[k+1] = max_index[k]
                            max_r[k] = r
                            max_index[k] = j
                            break
                        else:
                            max_r[k] = r
                            max_index[k] = j
        classify_dict[tags[i]] = [max_index[i] for i in range(member_len)]
        for t in range(member_len):
            choose_list[max_index[t]] = 1


    return classify_dict

def calculate_sokuji(classify_dict, scores_extract):
    sokuji_dict = dict()
    #print(classify_dict)
    for key, value in classify_dict.items():
        sokuji_dict[key] = 0
        for l in value:
            sokuji_dict[key] += scores_extract[l]
    sokuji_sorted = sorted(sokuji_dict.items(), key=lambda x:x[1], reverse=True)
    print("")
    for i in range(len(sokuji_sorted)):
        s = sokuji_sorted[i]
        print(s[0] + " " + str(s[1]) + " / ", end="")
    print("\n")

if __name__ == "__main__":
    setup_path()
    tags = user_input()
    names_image = separate_name()
    scores_image = separate_score()
    names_extract = analysis_name(names_image)
    scores_extract = analysis_score(scores_image)
    classify_dict = classify_name(tags, names_extract)
    calculate_sokuji(classify_dict, scores_extract)

