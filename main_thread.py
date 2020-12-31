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
        self.sleeping = False
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
            self.sleeping = False
            current_timestamp = int( time() )
            for bvid in self.bvid_to_video:
                video = self.bvid_to_video[bvid]
                print (video)
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
                    
            self.sleeping = True
            sleep(MIN_INTERVAL)
        self.STDSL.export_active_videos(self.bvid_to_video)
        self.exit()

    def shutdown(self):
        print ("Now exiting logger...")
        self.active = False
        while not self.sleeping:
            print ("Waiting for main thread to sleep")
            sleep(1)
        print ("Saving video data...")
        self.STDSL.export_active_videos(self.bvid_to_video)
        print ("Done!")

def main(mode: int):
    main_thread = MainThread(mode)
    main_thread.start()
    print ("executing main loop")
    while True:
        cmd = input("Type Q to shutdown logger.")
        if str(cmd) == "Q":
            break
    main_thread.shutdown()
    main_thread.join()

if __name__ == "__main__":
    main(FILE)
