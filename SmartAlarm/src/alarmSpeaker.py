""" alarmSleaker.py

    Summay:
        Alarm sleaker.
"""

import os
import cv2
import wave
import pyaudio
import random
import threading
from detectionSleepiness import DetectionSleepiness

class AlarmSpeaker:
    """ AlarmSpeaker. """

    # Sound path.
    __SOUNDS_DIR = "./sounds"

    def __init__(self):
        """ Init constructor.
        """
        self.__isRunning = False
        self.__speakerThreadObj = None
        self.__checkSleepinessThreadObj = None

    def __del__(self):
        """ Destructor.
        """
        self.stopThread()
     
    def goOff(self):
        """ Go off the alarm.
        """
        self.stopThread()
        self.startThread()

    def startThread(self):
        """ Start SpeakerThread and CheckSleepinessThread.
        """
        self.__isRunning = True
        if self.__speakerThreadObj is None:
            self.__speakerThreadObj = threading.Thread(target=self.__speakerThread)
            self.__speakerThreadObj.start()

        if self.__checkSleepinessThreadObj is None:
            self.__checkSleepinessThreadObj = threading.Thread(target=self.__checkSleepinessThread)
            self.__checkSleepinessThreadObj.start()

    def stopThread(self):
        """ Stop SpeakerThread and CheckSleepinessThread.
        """
        self.__isRunning = False
        if self.__speakerThreadObj is not None:
            self.__speakerThreadObj.join()
            self.__speakerThreadObj = None

        if self.__checkSleepinessThreadObj is not None:
            self.__checkSleepinessThreadObj.join()
            self.__checkSleepinessThreadObj = None

    def __checkSleepinessThread(self):
        """ Check sleepiness form the camera.
        """
        infApp = DetectionSleepiness()
        camera = cv2.VideoCapture(0)

        while self.__isRunning:
            _, frame = camera.read()
            if infApp.isSleepy(frame) == False:
                self.__isRunning = False

    def __speakerThread(self):
        """ Continue to sound music until stopped status.
        """
        sound = self.__SOUNDS_DIR + "/" + random.choice(os.listdir(self.__SOUNDS_DIR))

        while self.__isRunning:
            wf = wave.open(sound, "r")
            audio = pyaudio.PyAudio()
            stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

            data = wf.readframes(1024)

            while data != b'' and self.__isRunning:
                stream.write(data)
                data = wf.readframes(1024)
            
            stream.stop_stream()

            stream.close()
            audio.terminate()
            wf.close()
