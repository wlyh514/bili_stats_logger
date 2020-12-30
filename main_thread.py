from logger_thread import LoggerThread
from time import sleep, time
import threading
import fileSL
import databaseSL
from consts import *
from random import random


# enum
FILE = 1
DATABASE = 2

class MainThread(threading.Thread):

    def __init__(self, mode: int):
        threading.Thread.__init__(self)
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
        print("Logger now active...")
        while self.active:
            current_timestamp = int( time() )
            for bvid in self.bvid_to_video:
                video = self.bvid_to_video[bvid]

                if video["popularity"]["logging_end"] < current_timestamp:
                    self.STDSL.export_video(video)
                    del self.bvid_to_video[bvid]
                    continue

                if video["popularity"]["next_log"] == 0:
                    video["popularity"]["next_log"] = \
                        video["popularity"]["logging_interval"]
                    logger_thread = LoggerThread(video)
                    logger_thread.start()
                    sleep(1 + random())
                    

            sleep(MIN_INTERVAL)
        self.__shutdown__()
        self.exit()

    def __shutdown__(self):
        self.STDSL.export_active_videos(self.bvid_to_video)

def main(mode: int):
    main_thread = MainThread(mode)
    main_thread.start()
    print ("executing main loop")
    while True:
        cmd = input("Type Q to shutdown logger.")
        if str(cmd) == "Q":
            main_thread.active = False
            break
    print("Waiting for main thread to end")
    main_thread.join()

if __name__ == "__main__":
    main(FILE)
