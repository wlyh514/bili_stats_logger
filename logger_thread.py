import threading
from video_dict_constructor import new_video_dict
from loggers import VideoUpdateLogger

class LoggerThread(threading.Thread):
    """
    Updates all videos in bv_to_video dict, log all changes.  
    """
    # Override
    def __init__(self, bv_to_video: dict) -> None:
        super().__init__()
        self.bv_to_video = bv_to_video

    # Override
    def run(self):
        for bvid in self.bv_to_video:
            logger = VideoUpdateLogger(self.bv_to_video[bvid])
            logger.run()