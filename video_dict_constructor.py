from time import time
from consts import *

def construct_new_video_dict(response: dict)-> dict:
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
        }
    }

def update_video_dict(response: dict, video_dict: dict)-> None:
    pass