""" smartAlarm.py

    Summay:
        Smart Alarm application.
        This alarm will continue to sound until wake up.
"""

import cv2
import json
import time
import threading
from alarmSetting import AlarmSetting
from detectionSleepiness import DetectionSleepiness
from tcpClient import TCPClient
from datetime import datetime

class SmartAlarm:
    """ SmartAlram. """

    __SETTINGS_FILE = "/home/pi/SmartHomeProject/SmartAlarm/settings/alarmSettings.json"

    def __init__(self):
        """ Init constructor.
        """
        self.__isRunning = False
        self.__threadObj = None
        self.__alarmSettings = []
        self.__isRinging = False
        self.__checkSleepinessThreadObj = None
        self.__tcpClient = None

        self.readJson()
        self.startAlarmThread()
        
    def __del__(self):
        """ Destructor.
        """
        self.stopAlarmThread()
        self.writeJson()

    def addAlarmSetting(self, time: time, days: list):
        """ Add Alarm setting.
            (Example)
                addAlarmSetting(datetime.strptime("07:00", '%H:%M').time(),['Sun','Mon','Tue','Web','Thu','Fri'])

        Args:
            time (time): Alarm time.
            days (list): Days of the weeks.
        """
        setting = AlarmSetting(time.replace(second=0, microsecond=0),days)
        self.__alarmSettings.append(setting)

    def startAlarmThread(self):
        """ Start AlarmThread.
        """
        self.__isRunning = True
        if self.__threadObj is None:
            self.__threadObj = threading.Thread(target=self.__alarmThread)
            self.__threadObj.start()

    def stopAlarmThread(self):
        """ Stop AlarmThread.
        """
        self.__isRunning = False
        if self.__threadObj is not None:
            self.__threadObj.join()
            self.__threadObj = None
    
    def writeJson(self):
        """ Write the alarm settings to json file.
        """
        # Serialize the AlarmSetting object.
        list = []
        for alarm in self.__alarmSettings:
           if isinstance(alarm, AlarmSetting):
                alarm: AlarmSetting = alarm
                list.append(alarm.serialize())

        # Convert to json, write file.
        with open(self.__SETTINGS_FILE, mode='w', encoding='utf-8') as file:
            json.dump(list, file, indent = 2)

    def readJson(self):
        """ Read the alarm settings to json file.
        """
        with open(self.__SETTINGS_FILE, mode='r') as file:
            list = json.load(file)
            for setting in list:
                alarmSetting = AlarmSetting.deserialize(setting)
                if alarmSetting is not None:
                    self.__alarmSettings.append(alarmSetting)

    def __alarmThread(self):
        """ Main thread of SmartAlarm class.
            Check the alarm settings.
            If it matches the setting time, go off the alarm.
        """
        while self.__isRunning:
            if self.__checkAlram():
                self.__startRingAlarm()

            # Sleep until next time.
            time.sleep(60 - datetime.now().second)

    def __checkAlram(self) -> bool:
        """ Check the alarm settings

        Returns:
            (bool): Judgment value of check the alarm settings.
        """
        retVal = False
        now = datetime.now()
        for alarm in self.__alarmSettings:
           if isinstance(alarm, AlarmSetting):
               alarm: AlarmSetting = alarm
               # Check the alarm setting
               if alarm.isSetTime(now):
                   retVal = True
                   alarm.setEnabled(False)
        return retVal
    
    def __startRingAlarm(self):
        print("start ring")
        self.__isRinging = True
        if self.__checkSleepinessThreadObj is None:
            self.__checkSleepinessThreadObj = threading.Thread(target=self.__checkSleepinessThread)
            self.__checkSleepinessThreadObj.start()
        
        self.__tcpClient = TCPClient("192.168.40.60", 4000)
        self.__tcpClient.connect()
        self.__tcpClient.send_hex(bytes([0x01, 0x00]))
        
    def __checkSleepinessThread(self):
        """ Check sleepiness form the camera.
        """
        infApp = DetectionSleepiness()
        camera = cv2.VideoCapture("rtsp://192.168.40.60:8080/unicast")

        while self.__isRinging:
            _, frame = camera.read()
            if infApp.isSleepy(frame) == False:
                print("wake up")
                self.__isRinging = False
                self.__tcpClient.send_hex(bytes([0x01, 0x01]))
                self.__tcpClient.close()