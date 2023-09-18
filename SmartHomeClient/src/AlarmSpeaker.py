""" AlarmSleaker.py

    Summay:
        Alarm sleaker thread.
"""

import os
import time
import random
import threading
import simpleaudio

class AlarmSpeaker:
    """ AlarmSpeaker. """

    # Sound path.
    __SOUNDS_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../sounds"
    # Alarm timeout seconds
    __TIMEOUT = 2

    def __init__(self):
        """ Init constructor.
        """
        self.__isRunning = False
        self.__speakerThreadObj = None

    def __del__(self):
        """ Destructor.
        """
        self.StopThread()

    def StartThread(self):
        """ Start SpeakerThread and CheckSleepinessThread.
        """
        self.StopThread()
        self.__isRunning = True
        if self.__speakerThreadObj is None:
            self.__speakerThreadObj = threading.Thread(target=self.__speakerThread)
            self.__speakerThreadObj.start()

    def StopThread(self):
        """ Stop SpeakerThread and CheckSleepinessThread.
        """
        self.__isRunning = False
        if self.__speakerThreadObj is not None:
            self.__speakerThreadObj.join()
            self.__speakerThreadObj = None

    def __speakerThread(self):
        """ Continue to sound music until stopped status.
        """
        print("SpeakerThread start")
        start_time = time.time()
        sound_path = self.__SOUNDS_DIR + "/" + random.choice(os.listdir(self.__SOUNDS_DIR))

        while self.__isRunning:
            # read sound fime
            sound = simpleaudio.WaveObject.from_wave_file(sound_path)
            
            # speaker start
            play = sound.play()
            while play.is_playing() and self.__isRunning:
                time.sleep(1)
            
            # speaker stop
            play.stop()
            
            # determine timeout
            current_time = time.time()
            if current_time - start_time >= self.__TIMEOUT:
                self.__isRunning = False
                
        print("SpeakerThread stop")
