import re
import os

def strip_from_link(link: str):
    """
    Strip av/bv number from link. Return the link type(av/bv/none) and the striped id.
    Examples:
    >>> strip_from_link("https://www.bilibili.com/video/bv1H54y1t7Fm")
    ("bv", "BV1H54y1t7Fm")
    >>> strip_from_link("https://www.bilibili.com/video/av10492")
    ("av", "AV10492")
    >>> strip_from_link("some random string")
    ("none", "")
    """
    pass

def bv_to_av(bv: str):
    """
    Takes in a bvid bv and return its corresponding avid. 
    """
    pass

def av_to_bv(av: str):
    """
    Takes in an avid av and return its corresponding bvid.
    """
    pass

def find_all_files(path: str):
    for _, _, fs in os.walk(path):
        for f in fs:
            yield f
