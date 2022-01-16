import jieba
import os
import pathlib


def group_words(file_name, is_remove_common):
    jieba.load_userdict("userdict.txt")
    seg_comments = []
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~；。，！？、》《【】`″′（）+·—##：”“…~～'''
    if is_remove_common:
        punc = punc + '''的了我是不都你就啊吗有在好给这也看真的人这个吧还很说和就是能要没有什么不是但是呢可以多让被把怎么一个们了'''

    with open(file_name, "r") as file:
        for line in file:
            line = line
            seg_list = list(set(jieba.cut_for_search(line.upper())))  # 默认是精确模式
            seg_list = list(filter(lambda a: a.strip() not in punc, seg_list))
            seg_comments.append(seg_list)
    return seg_comments


def calculate_frequency(seg_list):
    word_count = {}
    for segment in seg_list:
        for word in segment:
            if word not in word_count:
                word_count[word] = 1
            else:
                word_count[word] += 1
    return word_count


def main():
    bvid = input("enter bvid")
    is_remove_common = input("remove common? Y/N")
    if is_remove_common.upper() == 'Y':
        is_remove_common = True
    else:
        is_remove_common = False
    seg_list = group_words(bvid+"/danmu.csv", is_remove_common)
    word_count = calculate_frequency(seg_list)
    word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    dir_name = os.path.join(pathlib.Path().resolve(), bvid)
    file_name = os.path.join(dir_name, "word_list.csv")
    with open(file_name, "w") as f:
        for key, value in word_count.items():
            f.write(str(value) + ", " + key + "\n")
    return word_count

