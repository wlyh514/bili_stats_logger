import json
from os import device_encoding
from consts import LOCAL_DATA_PATH, MAX_ACTIVE_VIDS, VIDEO_DYNAMIC_CHANGELOG_VERSION
from util import find_all_files
import time


def import_video(bvid: str)-> dict:
    current_timestamp = int( time.time() )
    try:
        f = open(f"{LOCAL_DATA_PATH}static/{bvid}.json", "r", encoding="utf-8")
    except FileNotFoundError:
        return {"TYPE": "ERROR-FileNotFound","bvid": bvid}
    video_dict = json.loads(f.read())
    f.close()
    video_dict["dynamics"] = {
        "TYPE": "VIDEO_DYNAMIC_CHANGELOG",
        "VERSION": "1.0",
        "bvid": video_dict["bvid"],

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
    video_dict["avaliable_time_intervals"].append({"start": current_timestamp, "end": current_timestamp})

    return video_dict
    

def import_active_videos(bvid_to_video: dict)-> None:

    f = open(LOCAL_DATA_PATH + "active_videos.txt", "r")
    line = f.readline().strip("\n")
    line_count = 1
    while line != "" and line_count < MAX_ACTIVE_VIDS:
        bvid_to_video[line] = import_video(line)
        line = f.readline().strip("\n")
        line_count += 1

    f.close()

def import_video_changelog(bvid: str, timestamp: int)-> dict:
    pass


def export_active_videos(bv_to_video: dict)-> None:
    # Export list of active videos to video_data/active_videos.txt
    f = open(LOCAL_DATA_PATH + "active_videos.txt", "w")
    for bvid in bv_to_video:
        if bv_to_video[bvid] == None:
            continue
        f.write(bvid + "\n")
    f.close()

    for bvid in bv_to_video:
        export_video(bv_to_video[bvid])

def export_video(video_dict: dict)-> None:
    bvid = video_dict["bvid"]
    # Remove the dynamic part from the video dict
    changelog = video_dict.pop("dynamics", None)

    # Export the static part of a video dict
    video_static = open(f"{LOCAL_DATA_PATH}static/{bvid}.json", "w", encoding="utf-8")
    json.dump(video_dict, video_static,ensure_ascii= False)
    video_static.close()
    
    # Export the dynamic part of a video dict
    export_video_changelog(changelog)


def export_video_changelog(changelog: dict)-> None:
    """
    Takes in the dynamic part of a video dict, and export it into a json file 
    under LOCAL_DATA_PATH/dynamic/bvid_start_end.json
    """
    bvid = changelog["bvid"]
    start = changelog["start"]
    end = changelog["end"]

    video_dynamic = open(f"{LOCAL_DATA_PATH}dynamic/{bvid}_{start}_{end}.json", "w", encoding="utf-8")
    json.dump(changelog, video_dynamic, ensure_ascii= False)
    video_dynamic.close()

if __name__ == "__main__":
    vids = {}
    import_active_videos(vids)