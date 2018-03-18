#!/usr/bin/python
#sudo apt-get install python-requests
import requests, json
import time

import os

iftttMakerKey = os.environ["IFTTTKEY"]

if environ.get("ISOTEMPDATADIR") is not None:
  logDir = os.environ["ISOTEMPDATADIR"]
else:
  logDir = "."

file = logDir + '/high_levels.json'
with open(file) as myfile:
    highDataLine = (list(myfile)[-1])

file = logDir + '/low_levels.json'
with open(file) as myfile:
    lowDataLine = (list(myfile)[-1])

file = logDir + '/ISOTEMPdata.log'
with open(file) as myfile:
    tempDataLine = (list(myfile)[-1])

urlPart1 = 'https://maker.ifttt.com/trigger/'
urlPart3 = '/with/key/' + iftttMakerKey

for x in range(5, 6):
    low = float(json.loads(lowDataLine)['tort' + str(x)])
    high = float(json.loads(highDataLine)['tort' + str(x)])
    temp = float(json.loads(tempDataLine)['tort' + str(x)])
    if (temp > high):
        #Send an IFTTT alert
        url = urlPart1 + 'tort' + str(x) + '_over_temp' + urlPart3
        values = {'value1' : 'tort' + str(x), 'value2' : temp, 'value3' : high}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        requestResponse = requests.post(url, data=json.dumps(values), headers=headers)
        print(requestResponse)
        print(request)
        time.sleep(5)
    elif (temp < low):
        #Send an IFTTT alert
        url = urlPart1 + 'tort' + str(x) + '_under_temp' + urlPart3
        values = {'value1' : 'tort' + str(x), 'value2' : temp, 'value3' : low}
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        requestResponse = requests.post(url, data=json.dumps(values), headers=headers)
        print(requestResponse)
        time.sleep(5)

