#!/usr/bin/env python

import os
import json
import requests

class libosd:
    uname = "user"
    passwd = "user1_pw"
    baseUrl = "osd.dynu.net"

    def __init__(self, cfg=None, baseUrl=None, uname=None, passwd=None):
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
                    self.baseUrl = jsonObj["baseurl"]
            else:
                print("ERROR - file %s does not exist" % cfg)
                exit(-1)
        else:
            print("No config file specified - using parameters")

        # Override config file parameters with command line parameters
        if (uname is not None):
            self.uname = uname
        if (passwd is not None):
            self.passwd = passwd
        if (baseUrl is not None):
            print("setting baseUrl")
            self.baseUrl = baseUrl

        print("baseUrl=%s, uname=%s, passwd=%s" %
              (self.baseUrl, self.uname, self.passwd))

        self.getToken()
        
    def getEvents(self, wearerId =1):
        print("libOsd.getEvents, wearerId=%d, baseUrl=%s" % (wearerId, self.baseUrl))
        urlStr = "%s/events" % self.baseUrl
        print("getEvents - urlStr=%s" % urlStr)
        retVal = self.getData(urlStr,None)
        return retVal

    def getEvent(self, eventId):
        print("libOsd.getEvent, eventId=%d, baseUrl=%s" % (eventId, self.baseUrl))
        urlStr = "%s/events/%d" % (self.baseUrl, eventId)
        print("getEvent - urlStr=%s" % urlStr)
        retVal = self.getData(urlStr,None)
        print("getEvent, returning: ",retVal)
        return retVal



    def addEvent(self, eventType, dataTime, desc, wearerId):
        data = {
            "eventType": eventType,
            "dataTime": dataTime,
            "desc" : desc,
            "userId": wearerId
            }
        urlStr = "%s/events/" % self.baseUrl
        print("addEvent - urlStr=%s" % urlStr)
        retVal = self.postData(urlStr,data)
        print("addEvent - retVal=",retVal)
        return retVal

    def updateEvent(self, eventId, eventType = None, dataTime = None, desc = None, wearerId = None):
        data = self.getEvent(eventId)
        print("updateEvent - eventId=%d, data=" % eventId,data)
        if (eventType is not None):
            data['eventType'] = eventType
        if (dataTime is not None):
            data['dataTime'] = dataTime
        if (desc is not None):
            data['desc'] = desc
        if (wearerId is not None):
            data['wearerId'] = wearerId
        urlStr = "%s/events/%d/" % (self.baseUrl, eventId)
        print("updateEvent - urlStr=%s" % urlStr)
        retVal = self.putData(urlStr,data)
        return retVal
        
 
    def uploadFile(self, fname, wearerId=1):
        print("libosd.uploadFile")
        #urlStr = "%s/datapoints/add.json" % self.baseUrl
        #urlStr = "%s/datapoints/" % self.baseUrl
        urlStr = "%s/uploadCsvData/" % self.baseUrl
        print("libosd: urlStr=%s" % urlStr)
        if (os.path.isfile(fname)):
            print("Opening file %s" % (fname))
            with open(fname) as infile:
                lineStr = "start"
                lineCount = 0
                #while (lineStr):
                #    lineStr = infile.readline()
                    # print(lineStr)
                #    self.postData(urlStr,
                #                  lineStr)
                    #lineStr = None
                lineStrs = infile.readlines()
                print("%d lines read from file" % len(lineStrs))
                self.postData(urlStr, lineStrs)
                print("libosd.uploadFile() - eof - linecount=%d" % lineCount)

    def postData(self, url, data):
        headerObj = {
                "Authorization": "Token %s" % self.token
        }
        #print("libosd.postData() - url=%s, data=%s" % (url, data))
        #print("libosd.postData() - headerObj=",headerObj)
        response = requests.post(
            url,
            headers=headerObj,
            #auth=(self.uname, self.passwd),
            json=data)
        # print("postData() - response=%s" % response.text)
        # print(response.status)
        # print(response.reason)
        print("libosd.postdata(): Status Code=%d" % response.status_code)
        # print(dir(response))
        print("libosd.postdata(): Response=", response.text)

    def putData(self, url, data):
        headerObj = {
                "Authorization": "Token %s" % self.token
        }
        #print("libosd.postData() - url=%s, data=%s" % (url, data))
        #print("libosd.postData() - headerObj=",headerObj)
        response = requests.put(
            url,
            headers=headerObj,
            #auth=(self.uname, self.passwd),
            json=data)
        # print("postData() - response=%s" % response.text)
        # print(response.status)
        # print(response.reason)
        print("libosd.putdata(): Status Code=%d" % response.status_code)
        # print(dir(response))
        print("libosd.putdata(): Response=", response.text)
        
    def getData(self, url, data,toObj=True):
        headerObj = {
                "Authorization": "Token %s" % self.token
        }
        #print("libosd.getData() - url=%s, data=%s" % (url, data))
        #print("libosd.getData() - headerObj=",headerObj)
        response = requests.get(
            url,
            headers=headerObj,
            #auth=(self.uname, self.passwd),
            json=data)
        # print("getData() - response=%s" % response.text)
        # print(response.status)
        # print(response.reason)
        print("libosd.getdata(): Status Code=%d" % response.status_code)
        # print(dir(response))
        if (toObj):
            retVal = json.loads(response.text)
        else:
            retVal = response.txt
        print("libosd.getdata(): Returning=", retVal)
        return(retVal)

        
    def getToken(self):
        print("getToken")
        urlStr = "%s/accounts/login/" % self.baseUrl
        print("urlStr=%s" % urlStr)
        response = requests.post(
            urlStr,
            json = {
                "login": self.uname,
		"password": self.passwd
                }
        )
        print("Status Code=%d" % response.status_code)
        if (response.status_code == 200):
            jsonObj = json.loads(response.text)
            self.token = jsonObj['token']
            print("token=%s" % self.token)
        else:
            self.token = None
            print("ERROR - Token not set")
        # print(dir(response))
        print(response.text)




        
        
if (__name__ == "__main__"):
    print("libosd.main()")
    osd = libosd(cfg="client.cfg", uname="graham4", passwd="testpwd1")
    #osd.uploadFile("DataLog_2019-11-04.txt", wearerId=3)
    eventsObj = osd.getEvents()
    print("eventsObj = ", eventsObj)

    retVal = osd.addEvent(eventType=4, dataTime="2021-11-30T20:35:00Z",
                          desc="testing addEvent",
                          wearerId=3)
    print("addEvent - retVal=",retVal)

    eventsObj = osd.getEvents()
    print("eventsObj = ", eventsObj)
    print(eventsObj['results'])

    retVal = osd.updateEvent(eventId=2, eventType=3)
    print(retVal)
