#!/usr/bin/env python

import os
import json
import requests

class libosd:
    uname = "user"
    passwd = "user1_pw"
    baseUrl = "osd.dynu.net"

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

        self.getToken()
        
    def uploadFile(self, fname, wearerId=1):
        print("libosd.uploadFile")
        #urlStr = "%s/datapoints/add.json" % self.baseurl
        #urlStr = "%s/datapoints/" % self.baseurl
        urlStr = "%s/uploadCsvData/" % self.baseurl
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

    def getToken(self):
        print("getToken")
        urlStr = "%s/accounts/login/" % self.baseurl
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
    osd = libosd(cfg="client.cfg", uname="user15", passwd="user_pw1234")
    osd.uploadFile("DataLog_2019-11-04.txt", wearerId=3)
