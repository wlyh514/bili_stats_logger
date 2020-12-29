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
            "basis": {
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
        }
    }

    return video_dict

def update_video_dict(response: dict, video_dict: dict)-> None:
    pass