from bilibili_api import comment, sync


async def main():
    # 存储评论
    comments = []
    # 页码
    page = 251
    # 当前已获取数量
    count = 0
    while True:
        # 获取评论
        c = await comment.get_comments(932422440, comment.ResourceType.VIDEO, page)
        # 存储评论
        comments.extend(c['replies'])
        # 增加已获取数量
        count += c['page']['size']
        # 增加页码
        page += 1
        if divmod(page, 5)[1] == 0:
            print("page: " + str(page) + " count: " + str(count))

        if count >= 5000:
            # 当前已获取数量已达到评论总数，跳出循环
            print("last page: " + str(page))
            break
    with open("/Users/Ying/Desktop/bilibili-scrape/comments_10000_1.csv", "w") as f:
        for cmt in comments:
            f.write((cmt['content']['message']).replace("\n", " ") + ";" + "\n")

sync(main())
