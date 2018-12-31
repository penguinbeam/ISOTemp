#!/usr/bin/python
#sudo apt-get install python-requests

#THIS SCRIPT IS DEPRECATED, support for IFTTT is no longer under development (why? because MiHome IFTTT doesn't support 4 way sockets properly...yet). Use parseNmiTrigger instead and register a Mihome API key to use their API directly.

import requests, json
import time
import os
from os import environ

iftttMakerKey = os.environ["IFTTTKEY"]

if environ.get("ISOTEMPDATADIR") is not None:
  logDir = os.environ["ISOTEMPDATADIR"]
else:
  logDir = "."

if environ.get("ISOTEMPBTSRC"):
  isBTSource = os.environ["ISOTEMPBTSRC"]
else:
  isBTSource = False
#isBTSource = False

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

if isBTSource:
    file = logDir + '/ISOTEMPbtdata.log'
else:
    file = logDir + '/ISOTEMPdata.log'
with open(file) as myfile:
    tempDataLine = (list(myfile)[-1])
    #Python keys can't have hyphens
    #tempDataLine = tempDataLine.replace('-','_')

urlPart1 = 'https://maker.ifttt.com/trigger/'
urlPart3 = '/with/key/' + iftttMakerKey

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
    #Now we've used the serial as the object key we can switch it back to a hyphen!
    #sensorKey = sensorKey.replace('_','-')
    print temp
    print high
    if (temp > high):
        #Send an IFTTT alert
        url = urlPart1 + sensorKey + '_over_temp' + urlPart3
        values = {'value1' : sensorKey, 'value2' : temp, 'value3' : high}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        requestResponse = requests.post(url, data=json.dumps(values), headers=headers)
        print(url)
        print(requestResponse)
        #print(values)
        time.sleep(5)
    elif (temp < low):
        #Send an IFTTT alert
        url = urlPart1 + sensorKey + '_under_temp' + urlPart3
        values = {'value1' : sensorKey, 'value2' : temp, 'value3' : low}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        requestResponse = requests.post(url, data=json.dumps(values), headers=headers)
        print(url)
        print(requestResponse)
        #print(values)
        time.sleep(5)
   # else:
   #     values = {'value1' : 'tort' + str(x), 'value2' : temp, 'value3' : low}
   #     print(values)
