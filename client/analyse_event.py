#!/usr/bin/python3

import argparse
import json
import libosd.webApiConnection
import libosd.osdAppConnection
import sys
import dateutil.parser
import time

import matplotlib.pyplot as plt


def dateStr2secs(dateStr):
    parsed_t = dateutil.parser.parse(dateStr)
    return parsed_t.timestamp()


def runTest():
    # Note, in test DB graham4 is a staff (researcher) user
    #              and graham29 is a normal user

    for unameStr in ("graham29", "graham4"):
        print("**********************")
        print("Trying as user %s" % unameStr)
        print("**********************")
        osd = libosd.libosd(cfg="client.cfg", uname=unameStr,
                            passwd="testpwd1", debug=True)
        eventsObj = osd.getEvents(userId=38)
        if (eventsObj is not None):
            for event in eventsObj:
                print(event)
        else:
            print("ERROR - No Data Returned");

        datapointsObj = osd.getDataPointsByEvent(eventId=395)
        if (datapointsObj is not None):
            for dp in datapointsObj:
                #print("dp=",dp)
                dpObj = json.loads(dp['dataJSON'])
                dataObj = json.loads(dpObj['dataJSON'])
                #print(dataObj.keys())
                print("%s, %d, %d, %.0f, %.0f, %.2f" % (dataObj['dataTime'],
                                                  dp['id'], dp['eventId'],
                                                  dataObj['specPower'],dataObj['roiPower'],
                                                  dataObj['roiPower']/dataObj['specPower']                                      ))
        else:
            print("ERROR - No Data Returned")

            
class EventAnalyser:
    configObj = None

    def __init__(self, configFname = "credentials.json"):
        print("EventAnalyser.__init__: configFname=%s" % configFname)
        self.loadConfig(configFname)
        print("self.configObj=",self.configObj)
        self.osd = libosd.webApiConnection.WebApiConnection(cfg="client.cfg",
                                 uname=self.configObj["uname"],
                                 passwd=self.configObj["passwd"],
                                 debug=True)
            
    def loadConfig(self,configFname):
        # Opening JSON file
        try:
            f = open(configFname)
            print("Opened File")
            self.configObj = json.load(f)
            f.close()
            print("configObj=",self.configObj)
        except BaseException as e:
            print("Error Opening File %s" % configFname)
            print("OS error: {0}".format(e))
            print(sys.exc_info())
            self.configObj = None

    def listEvents(self):
        eventsObj = self.osd.getEvents()
        if (eventsObj is not None):
            for event in eventsObj:
                print(event)
        else:
            print("ERROR - No Data Returned");


    def getEventDataPoints(self, eventId):
        eventObj = self.osd.getEvent(eventId)
        print("eventObj=", eventObj)
        dataPointsObj = self.osd.getDataPointsByEvent(eventId)
        # Make sure we are sorted into time order
        dataPointsObj.sort(key=lambda dp: dateStr2secs(dp['dataTime']))
        return(eventObj, dataPointsObj)

    def analyseEvent(self, eventId):
        print("analyse_event: eventId=%d" % eventId)
        eventObj, dataPointsObj = self.getEventDataPoints(eventId)
        alarmTime = dateStr2secs(eventObj['dataTime'])
        # FIXME - plan ahead for when we pass 3 direction values,
        #  not magnitude!
        rawDataType = 0  # 0 = magnitude, 1=3 directions.
        
        # Collect all the raw data into a single list with associated
        # time from the alarm (in seconds)
        rawTimestampLst = []
        accelLst = []
        analysisTimestampLst = []
        specPowerLst = []
        roiPowerLst = []
        roiRatioLst = []
        alarmRatioThreshLst = []
        alarmStateLst = []
        hrLst = []
        o2satLst = []
        for dp in dataPointsObj:
            currTs = dateStr2secs(dp['dataTime'])
            print(dp['dataTime'], currTs)
            dpObj = json.loads(dp['dataJSON'])
            dataObj = json.loads(dpObj['dataJSON'])
            print(dataObj)
            analysisTimestampLst.append(currTs - alarmTime)
            specPowerLst.append(dataObj['specPower'])
            roiPowerLst.append(dataObj['roiPower'])
            roiRatioLst.append(dataObj['roiPower']/dataObj['specPower'])
            alarmStateLst.append(dataObj['alarmState'])
            alarmRatioThreshLst.append(dataObj['alarmRatioThresh']/10.)
            hrLst.append(dataObj['hr'])
            o2satLst.append(dataObj['o2Sat'])

            # Add to the raw data lists
            accLst = dataObj['rawData']
            # FIXME:  IT is not good to hard code the length of an array!
            for n in range(0,125):
                accelLst.append(accLst[n])
                rawTimestampLst.append((currTs + n*1./25.)-alarmTime)

        #for n in range(0,len(rawTimestampLst)):
        #    print(n,rawTimestampLst[n],accelLst[n])
        fig, ax = plt.subplots()
        ax.plot(rawTimestampLst,accelLst)
        fig.savefig("plot.png")

        fig, ax = plt.subplots(4,1, figsize=(5,9))
        fig.suptitle('Event Number %d, %s\n%s, %s\n%s' % (
            eventId,
            eventObj['dataTime'],
            eventObj['type'],
            eventObj['subType'],
            eventObj['desc']),
                     fontsize=11)
        ax[0].plot(rawTimestampLst,accelLst)
        ax[0].set_title("Raw Data")
        ax[1].plot(analysisTimestampLst, specPowerLst)
        ax[1].plot(analysisTimestampLst, roiPowerLst)
        ax[1].set_title("Spectrum / ROI Powers")
        ax[2].plot(analysisTimestampLst, hrLst)
        ax[2].plot(analysisTimestampLst, o2satLst)
        ax[2].set_title("Heart Rate / O2 Sat")
        ax[3].plot(analysisTimestampLst, roiRatioLst)
        ax[3].plot(analysisTimestampLst, alarmRatioThreshLst)
        ax[3].plot(analysisTimestampLst, alarmStateLst)
        ax[3].set_title("ROI Ratio & Alarm State")
        fig.tight_layout()
        fig.subplots_adjust(top=0.85)
        fig.savefig("plot2.png")

    def testEvent(self, eventId, addr):
        ''' Retrieve event Number eventId from the remote database
        and feed its data to an OSD App at address addr.
        '''
        print("test_event: eventId=%d" % eventId)
        eventObj, dataPointsObj = self.getEventDataPoints(eventId)

        f = open("Event_%d_data.json" % eventId,"w")
        f.write(json.dumps(eventObj))
        f.write(json.dumps(dataPointsObj))
        f.close

        osdAppConnection = libosd.osdAppConnection.OsdAppConnection(addr)

        for dp in dataPointsObj:
            currTs = dateStr2secs(dp['dataTime'])
            print(dp['dataTime'], currTs)
            dpObj = json.loads(dp['dataJSON'])
            dataObj = json.loads(dpObj['dataJSON'])
            print(dataObj)
            
            # Create raw data list
            accelLst = []
            # FIXME:  IT is not good to hard code the length of an array!
            for n in range(0,125):
                accelLst.append(dataObj['rawData'][n])

            rawDataObj = {"dataType": "raw", "Mute": 0}
            rawDataObj['HR'] = dataObj['hr']
            rawDataObj['data'] = accelLst
            # FIXME - add o2sat
            dataJSON = json.dumps(rawDataObj)
            print(dataJSON)
            osdAppConnection.sendData(dataJSON)
            time.sleep(5)
        
            
if (__name__=="__main__"):
    print("analyse_event.py.main()")
    parser = argparse.ArgumentParser(description='analyse event')
    parser.add_argument('--config', default="credentials.json",
                        help='name of json file containing api login token')
    parser.add_argument('--event', default=None,
                        help='ID Number of the event to analyse')
    parser.add_argument('--list', action="store_true",
                        help='List all events in the database')
    parser.add_argument('--test',
                        help='Address of Device running OpenSeizureDetector Ap for Testing')
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    #analyse_event(configFname=args['config'])

    analyser = EventAnalyser(configFname=args['config'])

    if (args['event'] is not None):
        if (args['test'] is not None):
            print("Running Event Number %d on test server %s" %
                  (int(args['event']), args['test']))
            analyser.testEvent(int(args['event']), args['test'])
        else:
            print("Analysing Event Number %d" % int(args['event']))
            analyser.analyseEvent(int(args['event']))
    elif (args['list']):
        analyser.listEvents()
    else:
        print("Not doing anything")

