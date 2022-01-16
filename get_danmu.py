import os
import pathlib
from bilibili_api import video, sync


def get_danmakus(bvid, pid=0, save_raw=True):
    v = video.Video(bvid=bvid)
    dms = sync(v.get_danmakus(pid))
    dms = sorted(dms, key=lambda i: i.dm_time)
    dir_name = os.path.join(pathlib.Path().resolve(), bvid)
    pathlib.Path(dir_name).mkdir(parents=True, exist_ok=True)
    file_name = os.path.join(dir_name, ('p'+str(pid)+'_danmu.csv'))
    with open(file_name, 'w') as f:
        for dm in dms:
            f.write(f'{dm.text}' + '\n')
    if save_raw:
        raw_file_name = os.path.join(dir_name, ('p'+str(pid)+'_raw_danmu.csv'))
        with open(raw_file_name, 'w') as f:
            for dm in dms:
                f.write(f'{dm.crc32_id},{dm.dm_time},{dm.text}' + '\n')
    return dms

