#!/usr/bin/env python

import os
import json
import requests


class libosd:
    uname = "user"
    passwd = "user_pw"

    def __init__(self, cfg=None, baseurl=None, uname=None, passwd=None):
        print("libosd.__init__()")

        if (cfg is not None):
            if (os.path.isfile(cfg)):
                print("Opening file %s" % (cfg))
                with open(cfg) as infile:
                    jsonObj = json.load(infile)
                print(jsonObj)
                if ("uname" in jsonObj):
                    print("found uname - %s" % jsonObj["uname"])
                    self.uname = jsonObj["uname"]
                if ("passwd" in jsonObj):
                    print("found passwd - %s" % jsonObj["passwd"])
                    self.passwd = jsonObj["passwd"]
                if ("baseurl" in jsonObj):
                    print("found baseurl - %s" % jsonObj["baseurl"])
                    self.baseurl = jsonObj["baseurl"]
            else:
                print("ERROR - file %s does not exist" % cfg)
                exit(-1)
        else:
            print("No config file specified - using parameters")

        if (uname is not None):
            self.uname = uname
        if (passwd is not None):
            self.passwd = passwd
        if (baseurl is not None):
            print("setting baseurl")
            self.baseurl = baseurl

        print("baseurl=%s, uname=%s, passwd=%s" %
              (self.baseurl, self.uname, self.passwd))
        
    def uploadFile(self, fname, wearerId=1):
        print("uploadFile")
        if (os.path.isfile(fname)):
            print("Opening file %s" % (fname))
            with open(fname) as infile:
                lineStr = "start"
                lineCount = 0
                while (lineStr):
                    lineStr = infile.readline()
                    lineCount += 1
                    lineParts = lineStr.split(',')
                    lineObj = {}
                    lineObj['dateStr'] = lineParts[0]
                    fftArr = []
                    for n in range(0, 10):
                        fftArr.append(float(lineParts[n+1]))
                    lineObj['fftArr'] = fftArr
                    lineObj['specPower'] = float(lineParts[11])
                    lineObj['roiPower'] = float(lineParts[12])
                    lineObj['sampleFreq'] = float(lineParts[13])
                    lineObj['statusStr'] = lineParts[14].strip()
                    lineObj['hr'] = float(lineParts[15])
                    lineObj['wearerId'] = wearerId
                    rawDataArr = []
                    for n in range(16, len(lineParts)):
                        rawDataArr.append(float(lineParts[n]))
                    lineObj['rawData'] = rawDataArr
                    # jsonStr = json.dumps(lineObj)
                    # print(lineStr)
                    # print(lineObj)
                    # print(jsonStr)
                    urlStr = "%s/datapoints/add.json" % self.baseurl
                    print("urlStr=%s" % urlStr)
                    self.postData(urlStr,
                                  lineObj)
                    lineStr = None
                print("uploadFile() - eof - linecount=%d" % lineCount)

    def postData(self, url, data):
        print("postData() - url=%s, data=%s" % (url, data))
        response = requests.post(url,
                                 auth=(self.uname, self.passwd),
                                 json=data)
        # print("postData() - response=%s" % response.text)
        # print(response.status)
        # print(response.reason)
        print("Status Code=%d" % response.status_code)
        # print(dir(response))
        print(response.text)

        
if (__name__ == "__main__"):
    print("libosd.main()")
    osd = libosd(cfg="client.cfg", uname="analyst", passwd="analyst_pw")
    osd.uploadFile("DataLog_2019-11-04.txt", wearerId=1)
