#!/usr/bin/python3

import smbus
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
#pathFolder="/home/pi/MeineDateien/Light_AlarmSystem/"
FileNameLastAlarm="LastAlarm.txt"
FileNameLastWatchDog="LastWatchDog.txt"

LightLimit=5 #[Lux]
WatchDogTime=60*60 #in Seconds -->60Sek*60Min*12h --> 2 Packages per day. #todo
AlarmPause= 600 #in Seconds
AlarmText="ACHTUNG Seecontainer: Tür offen!"
pathTelegramSendScripts=pathFolder
bus = smbus.SMBus(1)

def convertToNumber(data):
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  data = bus.read_i2c_block_data(addr,0x20)
  return convertToNumber(data)   #return 2000 #debug #todo

def checkLightForAlarm(lux):
  if lux >= LightLimit:
    return True
  else:
    return False

def sendTelegramAlarmPackage(Light):
  #print("Alarm: "+AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")) #Debug
  
  #subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", AlarmText + "%0A" + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) #Testing only
  subprocess.run([pathTelegramSendScripts+"SendTelegram_SeeContainer.sh", AlarmText + "%0A" + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) #Prod System

def sendTelegramWatchDogPackage(Light):
  #print("WatchDog-Signal: " + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))  #Debug
  subprocess.run([pathTelegramSendScripts+"SendTelegram_Raspberry.sh", "WatchDog-Signal: " + dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S") +"%0A"+"Lichtwert (Lux): "+ str(Light)]) # "%0A" --> Line Break

def writeLastTimeToFile(filePath):
  currentTime=dt.datetime.now()
  try:
    fileLastAlarm = open(filePath,'w')
    try:
      fileLastAlarm.write(str(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
    except:
      print("Error write File.")
    finally:    
      fileLastAlarm.close()
  except:
    print("Error: Couldn't load file.")
    return -1

def readLastTimeFromFile(filePath):
  try:
    fileLastAlarm = open(filePath,'r')
    strLastAlarm=fileLastAlarm.read()
  except:
    print("Error: Couldn't load file.")
  finally:
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

  sendTelegramWatchDogPackage(999)
  lightLevel=readLight() #Initial Read Light Level.

  while True:
    #Check Alarmlevel
    try:
      lightLevel=readLight() #Read Light Level
      print (format(lightLevel,'.2f') + " lux") #Debug
    except Exception as e:
      print("Fehler I2C! "+ str(e))
      return -1
    
    #Alarm Check
    if checkLightForAlarm(lightLevel):
      print(str(diffLastEventToNow(pathFolder+FileNameLastAlarm)))
      if diffLastEventToNow(pathFolder+FileNameLastAlarm) >= AlarmPause:
        try:
          subprocess.Popen(["/home/pi/MeineDateien/webcamBildTelegramSend.sh"]) #Runs Webcam Skript and don't wait till finish
          sendTelegramAlarmPackage(lightLevel)
          writeLastTimeToFile(pathFolder+FileNameLastAlarm)
        except:
          print("Error: Couldn't send Telegram Message")
    else:
      #WatchDog Check - Send WatchDog Signal every n Seconds
      if diffLastEventToNow(pathFolder+FileNameLastWatchDog) >= WatchDogTime:
        try:
          sendTelegramWatchDogPackage(lightLevel)
          writeLastTimeToFile(pathFolder+FileNameLastWatchDog)
        except:
          print("Error: Couldn't send Telegram Message")
    
    time.sleep(20)

if __name__=="__main__":
   main()
