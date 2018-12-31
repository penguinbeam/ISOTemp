#!/usr/bin/python
import bluetooth

import time

import os
from os import environ

import re

if environ.get("DONTUSEREDIS"):
  useRedis = environ.get("DONTUSEREDIS")
else:
  useRedis = True

if useRedis:
  import redis
  redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)

#JSON log file for outputing temperatures
if environ.get("ISOTEMPDATADIR") is not None:
  logFilename = os.environ["ISOTEMPDATADIR"] + "/ISOTEMPbtdata.log"
else:
  logFilename = "./ISOTEMPbtdata.log"

#Bluetooth MAC of server logging temperatures centrally
btMasterMAC = os.environ["ISOTEMPBTMMAC"]

def receiveMessages():
  server_sock=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
  port = 3
  size = 1024
  backlog = 1
  server_sock.bind((btMasterMAC,port))
  server_sock.listen(backlog)
  print("Listener started")

  while 1:
    try:
      client_sock,clientAddress = server_sock.accept()
      data = client_sock.recv(size)
      if data:
        print "Accepted connection from " + str(clientAddress)
        if re.match("^[0-9][0-9]-[0-9a-f]+=[0-9]?[0-9]?[0-9]?.?[0-9]?[0-9]$", data):
          print "received [%s]" % data
          device = data.split("=")[0]
          temperature = data.split("=")[1]

          timestamp = time.strftime("%H:%M:%S %d/%m/%y")
          dataString = '\"' + device + '\":\"' + str(temperature) + '\"'

          dataLog = open(logFilename, "a", 1)
          dataLog.write('{\"timestamp\":\"' + timestamp + '\", ' + dataString + '}\n')
          dataLog.close()

          if useRedis:
            #Send each output to redis
            redis_db.delete(device)
            redis_db.lpush(device, *[temperature, timestamp])
        else:
          client_sock.send("You suck! Invalid data...")
          print "received crap data"
      client_sock.close()
    except Exception as e:
      print("Closing socket")
      print(e)
      break
  client_sock.close()
  server_sock.close()

receiveMessages()
