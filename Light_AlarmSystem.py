#!/usr/bin/python3

###import smbus
import time
import datetime as dt
from pathlib import Path
import subprocess

DEVICE     = 0x23
POWER_DOWN = 0x00
POWER_ON   = 0x01
RESET      = 0x07
LastAlarmFileName="LastAlarm.txt"
LightLimit=1000
AlarmPause= 600 #in Seconds
AlarmText="ACHTUNG Seecontainer: Tür offen!"
#bus = smbus.SMBus(1)

def convertToNumber(data):
  result=(data[1] + (256 * data[0])) / 1.2
  return (result)

def readLight(addr=DEVICE):
  #data = bus.read_i2c_block_data(addr,0x20)
  #return convertToNumber(data)
  return 2000

def checkLightForAlarm(lux):
  if lux >= LightLimit:
    return True
  else:
    return False
def sendTelegramAlarmPackage():
  print("Alarm: "+AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S"))
  #subprocess.run(["SendTelegram_Raspberry.sh", AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")])
  #subprocess.run(["SendTelegram_SeeContainer.sh", AlarmText + dt.datetime.now().strftime(" %Y-%m-%d %H:%M:%S")])

def writeLastAlarmTime():
  currentTime=dt.datetime.now()
  fileLastAlarm = open(LastAlarmFileName,'w')
  fileLastAlarm.write(str(currentTime.strftime("%Y-%m-%d %H:%M:%S")))
  fileLastAlarm.close()

def readLastAlarmTime():
  fileLastAlarm = open(LastAlarmFileName,'r')
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
  path = Path(LastAlarmFileName)
  if not path.is_file(): #Create File if it doesn't exist
    writeLastAlarmTime()

  #Check Alarmlevel
  lightLevel=readLight()
  print (format(lightLevel,'.2f') + " lux")
  if checkLightForAlarm(lightLevel):
    if diffLastAlarmToNow() >= AlarmPause:
      sendTelegramAlarmPackage()
      writeLastAlarmTime()


if __name__=="__main__":
   main()
