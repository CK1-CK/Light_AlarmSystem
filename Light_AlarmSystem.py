#!/usr/bin/python3

#import smbus
import time
import datetime as dt
from pathlib import Path
import subprocess
import pathlib

DEVICE     = 0x23
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07

pathFolder=str(pathlib.Path(__file__).parent.absolute())+"/"
FileNameLastAlarm="LastAlarm.txt"
FileNameLastWatchDog="LastWatchDog.txt"

LightLimit=1000
WatchDogTime=60*60 #60Sek*60Min*12h --> 2 Packages per day. #todo
AlarmPause= 600 #in Seconds
AlarmText="ACHTUNG Seecontainer: Tür offen!"
pathTelegramSendScripts=pathFolder
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

def sendTelegramAlarmPackage(Light):
  #print("Alarm: "+AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")) #Debug
  
  subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", AlarmText + "%0A" + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) #Testing only
  #subprocess.run([pathTelegramSendScripts+"SendTelegram_SeeContainer.sh", AlarmText + "%0A" + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) #Produktive System

def sendTelegramWatchDogPackage(Light):
  #print("WatchDog-Signal: " + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))  #Debug
  subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", "WatchDog-Signal: " + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) # "%0A" --> Line Break

def writeLastTimeToFile(filePath):
  currentTime=dt.datetime.now()
  fileLastAlarm = open(filePath,'w')
  fileLastAlarm.write(str(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
  fileLastAlarm.close()

def readLastTimeFromFile(filePath):
  fileLastAlarm = open(filePath,'r')
  strLastAlarm=fileLastAlarm.read()
  fileLastAlarm.close()
  return strLastAlarm

def diffLastEventToNow(filePath):
  currentTime=dt.datetime.now()
  strLastAlarm=readLastTimeFromFile(filePath)
  LastAlarm= dt.datetime.strptime(strLastAlarm, "%Y-%m-%d %H:%M:%S")
  delta = currentTime.replace(microsecond=0) - LastAlarm
  return delta.total_seconds()

def main():
  #Init
  pathAlarm = Path(pathFolder+FileNameLastAlarm)
  if not pathAlarm.is_file(): #Create File if it doesn't exist
    print("Alarm File not found")
    writeLastTimeToFile(pathFolder+FileNameLastAlarm)
  
  pathWatchDog = Path(pathFolder+FileNameLastWatchDog)
  if not pathWatchDog.is_file(): #Create File if it doesn't exist
    print("WatchDog File not found")
    writeLastTimeToFile(pathFolder+FileNameLastWatchDog)

  while True:
    #Check Alarmlevel
    lightLevel=readLight()
    #print (format(lightLevel,'.2f') + " lux") #Debug
    
    #Alarm Check
    if checkLightForAlarm(lightLevel):
      if diffLastEventToNow(pathFolder+FileNameLastAlarm) >= AlarmPause:
        sendTelegramAlarmPackage(lightLevel)
        writeLastTimeToFile(pathFolder+FileNameLastAlarm)
    else:
      #WatchDog Check - Send WatchDog Signal every n Seconds
      if diffLastEventToNow(pathFolder+FileNameLastWatchDog) >= WatchDogTime:
        sendTelegramWatchDogPackage(lightLevel)
        writeLastTimeToFile(pathFolder+FileNameLastWatchDog)
    
    time.sleep(30)

if __name__=="__main__":
   main()
