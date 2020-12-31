import threading
from video_dict_constructor import new_video_dict
from loggers import VideoUpdateLogger

class LoggerThread(threading.Thread):
    """
    Updates all videos in bv_to_video dict, log all changes.  
    """
    # Override
    def __init__(self, video_dict: dict) -> None:
        super().__init__()
        self.video_dict = video_dict

    # Override
    def run(self):
        print("Logger thread running...")
        logger = VideoUpdateLogger(self.video_dict)
        logger.run()
        print("Logger thread exited.")