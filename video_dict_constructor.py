from time import time
from consts import *

def new_video_dict(response: dict)-> dict:
    current_timestamp = int( time() )
    video_dict = {
        "TYPE": "VIDEO_LATEST_DATA",
        "VERSION": VIDEO_LATEST_DATA_VERSION,

        "bvid": response["data"]["bvid"],
        "timestamp": current_timestamp,

        "avaliable_time_intervals":[
            {
                "start": current_timestamp,
                "end": current_timestamp
            }
        ],

        "popularity": {
            "requested_ips" : [],
            "logging_interval": 60,
            "logging_end": 1608875287
        },

        "statics": {
            "aid":      response["data"]["aid"],
            "ownermid": response["data"]["owner"]["mid"],
            "pubdate":  response["data"]["pubdate"]
        },

        "semi-statics": {
            "latest": {
                "title":     response["data"]["title"],
                "desc":      response["data"]["desc"],
                "pages":     [page["part"] for page in response["data"]["pages"]],
                "pic":       response["data"]["pic"],
                "ownerface": response["data"]["owner"]["face"]
            }, 
            "changes": [

            ]
        },

        "stats": {
            "view":     response["data"]["stat"]["view"],
            "danmaku":  response["data"]["stat"]["danmaku"],
            "reply":    response["data"]["stat"]["reply"],
            "favorite": response["data"]["stat"]["favorite"],
            "coin":     response["data"]["stat"]["coin"],
            "share":    response["data"]["stat"]["share"],
            "like":     response["data"]["stat"]["like"]
        },

        "dynamics": {
            "TYPE": "VIDEO_DYNAMIC_CHANGELOG",
            "VERSION": "1.0",
            "bvid": response["data"]["bvid"],

            "start": current_timestamp,
            "end":   current_timestamp,
            "basis": {
                "view":     response["data"]["stat"]["view"],
                "danmaku":  response["data"]["stat"]["danmaku"],
                "reply":    response["data"]["stat"]["reply"],
                "favorite": response["data"]["stat"]["favorite"],
                "coin":     response["data"]["stat"]["coin"],
                "share":    response["data"]["stat"]["share"],
                "like":     response["data"]["stat"]["like"]
            },
            "changes":[

            ]
        }
    }

    return video_dict

def update_video_dict(response: dict, video_dict: dict)-> None:
    current_timestamp = int( time() )
    # Update timestamps
    video_dict["timestamp"] = current_timestamp
    video_dict["avaliabe_time_intervals"][-1]["end"] = current_timestamp
    video_dict["dynamics"]["end"] = current_timestamp

    # Update semi-statics
    new_semi_statics = {
        "title":     response["data"]["title"],
        "desc":      response["data"]["desc"],
        "pages":     [page["part"] for page in response["data"]["pages"]],
        "pic":       response["data"]["pic"],
        "ownerface": response["data"]["owner"]["face"]
    }
    for field_name in new_semi_statics:
        if new_semi_statics[field_name] != \
            video_dict["semi-statics"]["latest"][field_name]:
            changelog = {
                "timestamp": current_timestamp,
                "field_name": field_name,
                "old": video_dict["semi-statics"]["latest"][field_name],
                "new": new_semi_statics[field_name]
            }
            video_dict["semi-statics"]["changes"].append(changelog)
            video_dict["semi-statics"]["latest"][field_name] = new_semi_statics[field_name]
    
    # Update dynamics
    changelog = {
        "timestamp": current_timestamp
    }
    for field_name in video_dict["stats"]:
        diff = response["data"]["stat"][field_name] - video_dict["stats"][field_name]
        if diff != 0:
            changelog[field_name] = diff
            video_dict["stats"][field_name] += diff
    video_dict["dynamics"]["changes"].append(changelog)