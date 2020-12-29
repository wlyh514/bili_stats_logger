import json
from consts import LOCAL_DATA_PATH, MAX_ACTIVE_VIDS
from util import find_all_files
import time


def import_video(bvid: str)-> dict:
    current_timestamp = int( time.time() )
    try:
        f = open("%sstatic/%s.json" % (LOCAL_DATA_PATH, bvid))
    except FileNotFoundError:
        return {"TYPE": "ERROR-FileNotFound","bvid": bvid}

    video_dict = json.loads(f.read())
    f.close()
    video_dict["dynamics"] = {
        "start": current_timestamp,
        "end":   current_timestamp,
        "basis": {
            "view":    video_dict["stats"]["view"],
            "danmaku": video_dict["stats"]["danmaku"],
            "reply":   video_dict["stats"]["reply"],
            "favorite":video_dict["stats"]["favorite"],
            "coin":    video_dict["stats"]["coin"],
            "share":   video_dict["stats"]["share"],
            "like":    video_dict["stats"]["like"]
        },
        "changes": []
    }

    return video_dict
    

def import_active_videos(bvid_to_video: dict)-> None:
    try:
        f = open(LOCAL_DATA_PATH + "active_videos.txt")
    except FileNotFoundError:
        return

    line = f.readline()
    line_count = 1
    while line != "" and line_count < MAX_ACTIVE_VIDS:
        bvid_to_video[line] = import_video(line)
        line = f.readline()
        line_count += 1

    f.close()

def import_video_changelog(bvid: str, timestamp: int)-> dict:
    pass

def export_video():
    pass

def export_active_videos():
    pass

def export_video_changelog(changelog: dict)-> None:
    pass

if __name__ == "__main__":
    vids = {}
    import_active_videos(vids)