from logger_thread import LoggerThread
from time import sleep
import threading
import fileSL
import databaseSL
from consts import *


# enum
MODE = 0
FILE = 1
DATABASE = 2

class MainThread(threading.Thread):

    def __init__(self, mode: int):
        self.active = False

        if mode == FILE:
            self.STDSL = fileSL
        elif mode == DATABASE:
            self.STDSL = databaseSL

        self.bvid_to_video = {}
        self.__load__()
    
    def __load__(self):
        """
        Load videos from database / local files. 
        """
        self.STDSL.import_active_videos( self.bvid_to_video ) 

    def run(self):
        self.active = True
        while self.active:
            logger_thread = LoggerThread(self.bvid_to_video)
            logger_thread.run()
            sleep(MIN_INTERVAL)
        self.__shutdown__()

    def __shutdown__(self):
        self.STDSL.export_active_videos()

if __name__ == "__main__":
    mt = MainThread(FILE)
    mt.start()
