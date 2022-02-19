import aiohttp
import time


start_time = time.time()


async def main(dms, bvid, oid, start, end):
    dm_like_url = f'https://api.bilibili.com/x/v2/dm/thumbup/stats?oid={oid}&ids='
    dms_indexed_text = {}
    for dm in dms:
        dms_indexed_text[str(dm.id)] = {"text": dm.text, "dm_time": dm.dm_time}
    async with aiohttp.ClientSession() as session:
        print(f"start: {start}, end: {end}")
        for i in range(start, end, 100):
            dms_in_range = dms[i: i + 100]
            dms_ids = [str(dm.id) for dm in dms_in_range]
            dms_list_str = ",".join(dms_ids)
            dms_url = dm_like_url + dms_list_str
            print(f'Retrieving i: {i}')
            start = time.time()
            async with session.get(dms_url) as resp:
                dm_like = await resp.json()
                print("--- %s seconds ---" % (time.time() - start))
                try:
                    for dm_id in dm_like['data'].keys():
                        dms_indexed_text[dm_id]['likes'] = dm_like['data'][dm_id]['likes']
                except KeyError:
                    print(dms_url)
        dms_likes_list = [
            {"id": k, "text": v['text'], "likes": v['likes'], "dm_time": v['dm_time']}
            for k, v in dms_indexed_text.items()
        ]
        dms_likes_list = sorted(dms_likes_list, key=lambda item: item['likes'], reverse=True)
        with open(bvid + "/" + "dm_likes.csv", "w") as f:
            for line in dms_likes_list:
                f.write(f"{line['id']}, {line['text']}, {line['dm_time']}, {line['likes']}\n")
        print("--- %s seconds ---" % (time.time() - start_time))
        return dms_likes_list
