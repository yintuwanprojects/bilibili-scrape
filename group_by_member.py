import jieba
from get_danmu import get_danmakus

NAMES_LIST = {
    "刘宇": ["刘宇", "小宇", "宇子", "鱼宝", "宇宇", "liuyu", '劉宇'],
    "赞多": ["赞多", "贊多", "朵朵", "小多", "多多", "多子", "兜兜", "santa"],
    "力丸": ["力丸", "丸子", "丸酱", "riki", "rikimaru"],
    "米卡": ["米卡", "小咪", "mika"],
    "高卿尘": ["小九", "高卿尘", "小奈", "nine"],
    "林墨": ["momo", "林墨", "墨墨", "小墨", "linmo"],
    "伯远": ["伯远", "远哥", "伯老师", "伯劳斯", "啵远", "远酱", "远远"],
    "张嘉元": ["嘉元", "张嘉元", "元元", "元哥", "元儿哥", "小元", "元儿"],
    "尹浩宇": ["尹浩宇", "派派", "派比", "小派", "pat", "派翠", "patrick"],
    "周柯宇": ["柯宇", "周柯宇", "柯子", "丹尼尔", "周丹", "丹丹", "周科", "蛋妞", "daniel", "dan", "周柯"],
    "刘彰": ["ak", "小k", "刘彰", "k子", "鸭鸭", "彰彰", "鸭头", "k宝"],
    "INTO1": ["into1", "insider", "硬塞的", "硬塞得", "音兔万", "万人", "万粉"],
    "WJJW": ["wjjw", "哇唧唧哇", "wajijiwa", "挖机"]
}


def group_dm_by_user(dms):
    user_dms = {}
    for dm in dms:
        if dm.crc32_id not in user_dms.keys():
            user_dms[dm.crc32_id] = [dm.text]
        else:
            user_dms[dm.crc32_id].append(dm.text)
    return dict(sorted(user_dms.items(), key=lambda item: len(item[1]), reverse=True))


def get_word_frequency(dm_list):
    jieba.load_userdict("userdict.txt")
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~；。，！？、》《【】`″′（）+·—##：”“…~～'''
    punc = punc + '''的了我是不都你就啊吗有在好给这也看真的人这个吧还很说和就是能要没有什么不是但是呢可以多让被把怎么一个们了哈'''
    excluded = ["哈哈", "哈哈哈", "啊啊", "啊啊啊", "呵呵", "哈哈哈哈", "笑死"]
    dm_segs = []
    for dm in dm_list:
        seg_list = list(set(jieba.cut_for_search(dm.lower())))  # 默认是精确模式
        seg_list = list(filter(lambda a: (a.strip() not in punc) and (a.strip() not in excluded), seg_list))
        dm_segs = dm_segs + seg_list
    word_count = {}
    for word in dm_segs:
        if word in word_count and word != '':
            word_count[word] += 1
        elif word != '':
            word_count[word] = 1
    return sorted([{"word": k, "freq": v} for k, v in word_count.items()], key=lambda item: item["freq"], reverse=True)


def get_tag_from_word_freq(word_freq):
    tag = ""
    for wf in word_freq[:10]:
        if tag == "":
            tag = wf["word"]
        for k in NAMES_LIST.keys():
            if wf["word"] in NAMES_LIST[k]:
                return k
    return tag


def group_user_dm_by_member(user_dms):
    user_dm_tagged = []
    for k, v in user_dms.items():
        top_words = get_word_frequency(v)
        tag = get_tag_from_word_freq(top_words)
        user_dm_tagged.append({"user": k, "dm_count": len(v), "top5_words": top_words[:5], "tag": tag})
    return user_dm_tagged


def get_tag_count_by_member(grouped_user_dms):
    tag_count = {}
    for user_dm in grouped_user_dms:
        if user_dm['tag'] not in tag_count.keys():
            tag_count[user_dm['tag']] = []
        tag_count[user_dm['tag']].append(user_dm['dm_count'])
    # print(tag_count)
    return sorted([{"tag": k, "count": len(v), "avg": "{:.2f}".format((sum(v)/len(v)))} for k, v in tag_count.items()],
                  key=lambda i: i['count'],
                  reverse=True)


if __name__ == '__main__':
    bvid = input("enter bvid: \n")
    danmus = get_danmakus(bvid)
    user_danmus = group_dm_by_user(danmus)
    grouped_user_danmus = group_user_dm_by_member(user_danmus)
    tag_counts = list(filter(lambda a: a["count"] > 1, get_tag_count_by_member(grouped_user_danmus)))
    with open(f"{bvid}/dms_tag_counts.csv", "w") as f:
        f.write("词条, 人数, 人均弹幕数\n")
        for tag in tag_counts:
            f.write(f'{tag["tag"]}, {tag["count"]}, {tag["avg"]}\n')
    print("done")
