#!/usr/bin/env python
"""
Python interface to the published static OSD seizure database
"""

import os
import json
import dateutil.parser

def dateStr2secs(dateStr):
    parsed_t = dateutil.parser.parse(dateStr)
    return parsed_t.timestamp()

def extractJsonVal(row, elem, debug=False):
    if (debug): print("extractJsonVal(): row=",row)
    dataJSON = row['dataJSON']
    if (dataJSON is not None):
        if (debug): print("extractJsonVal(): dataJSON=",dataJSON)
        dataObj = json.loads(dataJSON)
        if (elem in dataObj.keys()):
            elemVal = dataObj[elem]
        else:
            elemVal = None
    else:
        elemVal = None
    return(elemVal)

class OsdDbConnection:
    DEBUG = False
    cacheDir = os.path.join(os.path.expanduser("~"),"osd/osdb")
    cacheFname = "osdb"  # base of filename
    download = True
    maxEvents = 10000
    eventsLst = []

    def __init__(self, cacheDir = None, debug=False):
        self.DEBUG = debug
        if (self.DEBUG): print("libosd.OsdDbConnection.__init__()")
        if (cacheDir is not None):
            self.cacheDir = cacheDir

        if (self.DEBUG): print("cacheDir=%s, debug=%s" %
              (self.cacheDir, self.DEBUG))

    def loadDbFile(self, fname):
        ''' Retrieve a list of events data from a json file
        '''
        fpath = os.path.join(self.cacheDir, fname)
        if (self.DEBUG): print("OsdDbConnection.loadDbFile - fpath=%s" % fpath)
        fp = open(fpath,"r")
        self.eventsLst.extend(json.load(fp))
        fp.close()
        return(len(self.eventsLst))

            
    def getEvent(self, eventId, includeDatapoints=False):
        for event in self.eventsLst:
            if (event['id']==eventId):
                return event
        print("Event not found in cache")
        return None

    def listEvents(self):
        for event in self.eventsLst:
<<<<<<< HEAD
            print("%d, %s, %d, %s, %s, %s" %
=======
            phoneAppVersion = extractJsonVal(event,"phoneAppVersion",False)
            dataSource = extractJsonVal(event,"dataSourceName",False)
            watchSdName =extractJsonVal(event,"watchSdName",False)
            watchSdVersion =extractJsonVal(event,"watchSdVersion",False)
            print("%d, %s, %d, %s, %s, %s, %s, %s, %s, %s" %
>>>>>>> upstream/master
                  (event['id'],
                   event['dataTime'],
                   event['userId'],
                   event['type'],
                   event['subType'],
<<<<<<< HEAD
=======
                   phoneAppVersion,dataSource, watchSdName, watchSdVersion,
>>>>>>> upstream/master
                   event['desc']
                   ))

    
if (__name__ == "__main__"):
    print("libosd.osdDbConnection.main()")
    osd = OsdDbConnection(debug=True)
<<<<<<< HEAD
    eventsObjLen = osd.loadDbFile("osdb_tcSeizures.json")
    eventsObjLen = osd.loadDbFile("osdb_allSeizures.json")
    eventsObjLen = osd.loadDbFile("osdb_falseAlarms.json")
    eventsObjLen = osd.loadDbFile("osdb_unknownEvents.json")
=======
    #eventsObjLen = osd.loadDbFile("osdb_tcSeizures.json")
    #eventsObjLen = osd.loadDbFile("osdb_allSeizures.json")
    eventsObjLen = osd.loadDbFile("osdb_falseAlarms.json")
    #eventsObjLen = osd.loadDbFile("osdb_unknownEvents.json")
>>>>>>> upstream/master
    osd.listEvents()
    print("eventsObjLen=%d" % eventsObjLen)
    #eventsObjLen = osd.getEvents()
    #print("eventsObj = ", eventsObj)
    #print(eventsObj['results'])

