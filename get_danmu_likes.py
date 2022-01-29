import aiohttp
import asyncio
import time
import get_danmu

start_time = time.time()


async def main(dms, bvid, oid, start, end):
    dm_like_url = f'https://api.bilibili.com/x/v2/dm/thumbup/stats?oid={oid}&ids='
    dms_indexed_text = {}
    async with aiohttp.ClientSession() as session:
        print(f"start: {start}, end: {end}")
        for i in range(start, end, 20):
            dms_in_range = []
            for j in range(0, 20):
                if (int(i) + int(j)) < len(dms):
                    dms_in_range.append(dms[int(i) + int(j)])
            dms_ids = [str(dm.id) for dm in dms_in_range]
            dms_list_str = ",".join(dms_ids)
            dms_url = dm_like_url + dms_list_str
            for dm in dms_in_range:
                dms_indexed_text[str(dm.id)] = {"text": dm.text, "dm_time": dm.dm_time}
            async with session.get(dms_url) as resp:
                dm_like = await resp.json()
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
        return dms_likes_list

print("--- %s seconds ---" % (time.time() - start_time))
