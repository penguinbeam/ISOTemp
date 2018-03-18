#!/usr/bin/python
#Imports for interrupt handling
import time, sys
import signal

#Imports for thermo files discover
from subprocess import check_output
import re

import bluetooth

import os
from os import environ

#Most likely /sys/bus/w1/devices/
thermoSensorPath = os.environ["ISOTEMPSENSORPATH"]

#Bluetooth MAC of server logging temperatures centrally - not required if all sensors and logs etc. are on one device
btMasterMAC = os.environ["ISOTEMPBTMMAC"]

#JSON log file for outputing temperatures
if environ.get("ISOTEMPDATADIR") is not None:
  logFilename = os.environ["ISOTEMPDATADIR"] + "/ISOTEMPdata.log"
else:
  logFilename = "./ISOTEMPdata.log"


if environ.get("ISOTEMPBTS") is not None:
  isBTSlave = os.environ["ISOTEMPBTS"]
else:
  isBTSlave = False

def sendBTMessageTo(targetBluetoothMacAddress,message):
  port = 3
  sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  sock.connect((targetBluetoothMacAddress, port))
  sock.send(message)
  sock.close()

class GracefulInterruptHandler(object):

    def __init__(self, sig=signal.SIGINT):
        self.sig = sig

    def __enter__(self):

        self.interrupted = False
        self.released = False

        self.original_handler = signal.getsignal(self.sig)

        def handler(signum, frame):
            self.release()
            self.interrupted = True

        signal.signal(self.sig, handler)

        return self

    def __exit__(self, type, value, tb):
        self.release()

    def release(self):

        if self.released:
            return False

        signal.signal(self.sig, self.original_handler)

        self.released = True

        return True

#Find files in directory that look like w1 thermometer files
r = re.compile("^[0-9][0-9]-[0-9a-f]+")
thermoDevFileList = check_output(["ls", thermoSensorPath])
thermoDevFileList = thermoDevFileList.split('\n')
thermoDevFiles = filter(r.match, thermoDevFileList)

with GracefulInterruptHandler() as h:
        while True:
                timestamp = time.strftime("%H:%M:%S %d/%m/%y")
                tempForLog = [];

                for x in xrange(0, len(thermoDevFiles)):

                        openFile = open(thermoSensorPath +'/'+ thermoDevFiles[x] +'/'+ "w1_slave")
                        fileText = openFile.read()
                        openFile.close()

                        temperature_data = fileText.split()[-1]
                        temperature = float(temperature_data[2:])
                        temperature = temperature / 1000
                        tempForLog.append(round(temperature, 2));

                if isBTSlave:
                       sendBTMessageTo(btMasterMAC, thermoDevFiles[x] +'='+ str(tempForLog[x]))

                dataLog = open(logFilename, "a", 1)
                dataLog.write('{\"timestamp\":\"' + timestamp + '\",\"' + thermoDevFiles[x] + '\":\"' + str(tempForLog[x]) + '\"}\n')
                dataLog.close()

                time.sleep(300)
                if h.interrupted:
                        print "\nClosing gracefully"
                        dataLog.close()
                        break

