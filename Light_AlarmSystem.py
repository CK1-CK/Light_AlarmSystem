#!/usr/bin/python3

#import smbus
import time
import datetime as dt
from pathlib import Path
import subprocess

DEVICE     = 0x23
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07
pathLastAlarmFileName="/home/pi/MeineDateien/LastAlarm.txt"
LightLimit=1000
WatchDogTime=60*60 #60Sek*60Min*24Min --> OnePackage per day. Either Alarm or Watchdog Package
AlarmPause= 600 #in Seconds
AlarmText="ACHTUNG Seecontainer: Tür offen!"
pathTelegramSendScripts="/home/pi/MeineDateien/"
#bus = smbus.SMBus(1)

def convertToNumber(data):
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
 # data = bus.read_i2c_block_data(addr,0x20)
  #return convertToNumber(data)
  return 2000 #debug #todo

def checkLightForAlarm(lux):
  if lux >= LightLimit:
    return True
  else:
    return False

def checkTimeForWatchDog(timeInSeconds, lux):
  if diffLastAlarmToNow() >= timeInSeconds:
    sendTelegramWatchDogPackage(lux)

def sendTelegramAlarmPackage():
  print("Alarm: "+AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))
  
  subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", "WatchDog-Signal: " + "%0A" + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")]) #Testing only
  #subprocess.run([pathTelegramSendScripts+"SendTelegram_SeeContainer.sh", AlarmText + "%0A" + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")]) #Produktive System

def sendTelegramWatchDogPackage(Light):
  #print("WatchDog-Signal: " + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))  #Debug
  subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", "WatchDog-Signal: " + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) # "%0A" --> Line Break

def writeLastAlarmTime():
  currentTime=dt.datetime.now()
  fileLastAlarm = open(pathLastAlarmFileName,'w')
  fileLastAlarm.write(str(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
  fileLastAlarm.close()

def readLastAlarmTime():
  fileLastAlarm = open(pathLastAlarmFileName,'r')
  strLastAlarm=fileLastAlarm.read()
  fileLastAlarm.close()
  return strLastAlarm

def diffLastAlarmToNow():
  currentTime=dt.datetime.now()
  strLastAlarm=readLastAlarmTime()
  LastAlarm= dt.datetime.strptime(strLastAlarm, "%Y-%m-%d %H:%M:%S")
  delta = currentTime.replace(microsecond=0) - LastAlarm
  return delta.total_seconds()

def main():
  #Init
  path = Path(pathLastAlarmFileName)
  if not path.is_file(): #Create File if it doesn't exist
    writeLastAlarmTime()

  #Check Alarmlevel
  lightLevel=readLight()
  print (format(lightLevel,'.2f') + " lux")
  if checkLightForAlarm(lightLevel):
    if diffLastAlarmToNow() >= AlarmPause:
      sendTelegramAlarmPackage()
      writeLastAlarmTime()

  checkTimeForWatchDog(WatchDogTime, lightLevel) #Send WatchDog Signal every n Seconds


if __name__=="__main__":
   main()
