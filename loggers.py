from json.decoder import JSONDecodeError
from user_agent import generate_navigator
from exceptions import *
from time import time
from consts import *
import requests
import json



VIDEO_INFO_API = "https://api.bilibili.com/x/web-interface/view?bvid={bvid}"


class VideoInfoLogger(object):
    """
    Takes in a video dict, get video information from api.bilibili.com
    """

    def __init__(self, video_dict: dict):
        self.video_dict = video_dict
        self.response_str = ""

    def __request__(self)-> None:
        """
        Request video information save raw response as self.response_str
        """
        url = VIDEO_INFO_API.format(bvid = self.video_dict["bvid"])
        ua = generate_navigator()
        response = requests.get(url, headers = ua)
        self.response_str = response.text
        
    def __update_data__(self)-> None:
        """
        Parse the json code from api.bilibili.com to a dict(self.response_dict).
        Update / Finish self.video_dict from self.response_dict
        """
        self.response_dict = json.loads(self.response_str)
        response_code = self.response_dict["code"]
        if response_code != 0:
            raise BilibiliAPIException(response_code)

    def run(self) -> None:
        self.__request__()
        self.__update_data__()

class UpdateVideoInfo(VideoInfoLogger):
    """
    Takes in a video dict, get video information from api.bilibili.com
    And update the video dict(only minimum modifications on dynamics section).
    """
    def __init__(self, video_dict: dict):
        super().__init__(video_dict)
    
    # Override
    def __update_data__(self) -> None:
        super().__update_data__()



class GetNewVideoInfo(VideoInfoLogger):
    """
    Takes in a video dict (with only bivd field), get video information from api.bilibili.com
    And fill in all required data.
    """
    def __init__(self, video_dict: dict):
        super().__init__(video_dict)
    
    # Override
    def __update_data__(self) -> None:
        pass

if __name__ == "__main__":
    cnl = VideoInfoLogger("BV1H54y1t7Fm")
    print(cnl.run())