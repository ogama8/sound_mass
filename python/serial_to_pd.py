"""
serial_to_pd.py - Written Spring 2015 by Eli Backer for IME457, Prof. Tali Freid
"""

import serial
import os
import time

def sendtopd (message=' ', port='3000'):
   os.system("cd //Applications/Pd-extended.app/Contents/Resources/bin/ && echo '" + message + ";' | ./pdsend " + str(port))


tagDict   = {'0' : 0}
totalTags = 0
numReads  = 0

print '\033[93m' + "This code forces the reader to use antennas 0 and 1, which can cause serious damage to the reader if those antennas are not connected." + '\033[0m'
raw_input("Press Enter to continue...")
print ""
print " -----"
print ""

ser = serial.Serial('/dev/cu.usbserial', 115200, timeout=0.1)
print ser.name

ser.write("AntennaSequence = 0 1\r")
print ser.read(1000)
ser.write("TagListFormat = Custom\r")
print ser.read(1000)
ser.write("TagListCustomFormat = ${TX} ${TAGID} ${RSSI}\r")
print ser.read(1000)

time.sleep(1)

try:
   while True:
      try:
         ser.write("t\r")
         lines = ser.readlines()

         for line in lines:
            if len(line) > 25:
               packet = line[:-2].replace(".", "", 1).split()

               ant  = int(float(packet[0]))
               tag  =           packet[1]
               RSSI = int(float(packet[2]))

               print str(numReads).rjust(5) + ":  ", ant, tag, RSSI

               if tag not in tagDict:
                  totalTags += 1
                  tagDict[tag] = totalTags

               sendtopd(str(ant),          3000)
               sendtopd(str(tagDict[tag]), 3001)
               sendtopd(str(RSSI),         3002)

         time.sleep(0.1)
         numReads += 1
         print
      except IndexError:
         pass

except KeyboardInterrupt:
   ser.close()
   print "\n\nCaught the KeyboardInterrupt and closed the serial connection; quitting."
