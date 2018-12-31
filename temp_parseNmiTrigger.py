#!/usr/bin/python
#sudo apt-get install python-requests
import requests, json
import time
import os
from os import environ
from datetime import datetime

print (str(datetime.now()))

miUser = os.environ["MIUSER"]
miPass = os.environ["MIPASS"]

if environ.get("ISOTEMPDATADIR") is not None:
  logDir = os.environ["ISOTEMPDATADIR"]
else:
  logDir = "."

if environ.get("ISOTEMPBTSRC"):
  isBTSource = os.environ["ISOTEMPBTSRC"]
else:
  isBTSource = False
#isBTSource = False

if environ.get("DONTUSEREDIS"):
  useRedis = environ.get("DONTUSEREDIS")
else:
  useRedis = True

file = logDir + '/high_levels.json'
with open(file) as myfile:
    highDataLine = (list(myfile)[-1])
    #Python keys can't have hyphens
    #highDataLine = highDataLine.replace('-','_')

file = logDir + '/low_levels.json'
with open(file) as myfile:
    lowDataLine = (list(myfile)[-1])
    #Python keys can't have hyphens
    #lowDataLine = lowDataLine.replace('-','_')

if useRedis:
    import redis
    redis_db = redis.StrictRedis(host="localhost", port=6379, db=0)
    tempKeys = redis_db.keys()
    ### TODO ### I think this next line is hardcoded junk for testing, check and remove...
    redis_db.lrange('28-000006532e6e',0,-1)
    tempDataLineFrag = ""
    for x in xrange(0, len(tempKeys)):
        tempDataLineFrag += ', "'+tempKeys[x]+'":"'+str(redis_db.lrange(tempKeys[x],0,-1)[1])+'"'
    tempDataLine = '{"timestamp":"'+str(redis_db.lrange(tempKeys[0],0,-1)[0])+'"'+tempDataLineFrag+'}'

else:
    if isBTSource:
        file = logDir + '/ISOTEMPbtdata.log'
    else:
        file = logDir + '/ISOTEMPdata.log'
    with open(file) as myfile:
        tempDataLine = (list(myfile)[-1])
        #Python keys can't have hyphens
        #tempDataLine = tempDataLine.replace('-','_')

#Extract all sensor names/serial numbers from log
sensorList=[]
data = json.loads(tempDataLine)
data.pop('timestamp', 0)
for key, value in data.iteritems():
    temp = [key,value]
    sensorList.append(temp)

#For each sensor look up its value from the log data
for x in range(0, len(sensorList)):
    sensorKey = str(sensorList[x][0])
    high = float(json.loads(highDataLine)[sensorKey])
    temp = float(json.loads(tempDataLine)[sensorKey])
    low = float(json.loads(lowDataLine)[sensorKey])

    #print(x)
    #print(high)
    #print(temp)
    #print(low)

    #Look up each sensor ID to find a tortoise and plug ID
    file =  logDir + "/tort2devicemap.json"
    with open(file) as myfile:
        map = (list(myfile)[-1])

    tortoise=json.loads(map)[sensorKey][0]
    plugId=json.loads(map)[sensorKey][1]
    plugSocket=json.loads(map)[sensorKey][2]
    if plugId != "":
         plugId=int(plugId)

         if plugSocket == "":
             plugSocket=None
             values = {'id' : plugId}
         else:
             plugSocket=int(plugSocket)
             values = {'id' : plugId, 'socket' : plugSocket}
         headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
         if (temp > high):
             url = "https://mihome4u.co.uk/api/v1/subdevices/power_off"
             requestResponse = requests.post(url, data=json.dumps(values), headers=headers, auth=(miUser, miPass))
             print(tortoise + ' too hot')
             print(requestResponse)
         elif (temp < low):
             url = "https://mihome4u.co.uk/api/v1/subdevices/power_on"
             requestResponse = requests.post(url, data=json.dumps(values), headers=headers, auth=(miUser, miPass))
             print(tortoise + ' cold')
             print(requestResponse)
         else:
             print(tortoise + ' ok')
    time.sleep(5)
