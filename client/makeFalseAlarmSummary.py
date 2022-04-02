#!/usr/bin/python3

import datetime
import dateutil.parser
import os
import argparse
import json
import tempfile
import jinja2
import numpy as np
import distutils.dir_util

import libosd.analyse_event
import libosd.webApiConnection
import libosd.loadConfig

import pandas as pd


def downloadData(userId, configFname, maxEvents=1000):
    configObj = libosd.loadConfig.loadConfig(configFname)
    outDir = os.path.join("output","False_alarm_summary_user_%s" % userId)
    os.makedirs(outDir, exist_ok=True)
    print("makeFalseAlarmSummary - outDir=%s" % outDir)

    osd = libosd.webApiConnection.WebApiConnection(cfg="client.cfg",
                                 uname=configObj["uname"],
                                 passwd=configObj["passwd"],
                                                   debug=False)
    analyser = libosd.analyse_event.EventAnalyser(configFname=args['config'], debug=False)

    if (userId=="all"):
        eventsObj = osd.getEvents(userId=None)
    else:
        eventsObj = osd.getEvents(userId=userId)
    for event in eventsObj:
        print(event)
    eventLst = []
    count = 0
    for event in eventsObj:
        #if (event['type'] is not None and event['type'] != 'Unknown'):
        if True:
            print("%5d %s %s %s %s" % (event['id'],
                                       event['dataTime'],
                                       event['type'],
                                       event['subType'],
                                       event['desc']
                                       ))
            analyser.loadEvent(event['id'])
            # Extract data from first datapoint to get OSD settings
            #     at time of event.
            if len(analyser.dataPointsObj)!=0:
                dp=analyser.dataPointsObj[0]
                dpObj = json.loads(dp['dataJSON'])
                dataObj = json.loads(dpObj['dataJSON'])

                eventSummaryObj = {}
                eventSummaryObj['id'] = event['id']
                eventSummaryObj['userId'] = event['userId']
                eventSummaryObj['dataTimeStr'] = dateutil.parser.parse(
                    analyser.eventObj['dataTime']).strftime("%Y-%m-%d %H:%M")
                eventSummaryObj['type'] = event['type']
                eventSummaryObj['subType'] = event['subType']
                eventSummaryObj['osdAlarmState'] = event['osdAlarmState']
                eventSummaryObj['desc'] = event['desc']
                eventSummaryObj['maxRoiRatio'] = max(analyser.roiRatioLst)
                eventSummaryObj['minRoiAlarmPower'] = analyser.minRoiAlarmPower
                eventSummaryObj['alarmFreqMin'] = dataObj['alarmFreqMin']
                eventSummaryObj['alarmFreqMax'] = dataObj['alarmFreqMax']
                eventSummaryObj['alarmThreshold'] = dataObj['alarmThresh']
                eventSummaryObj['alarmRatioThreshold'] = dataObj['alarmRatioThresh']
                eventSummaryObj['datapoints'] = analyser.dataPointsObj

                eventLst.append(eventSummaryObj)
            else:
                print("Ignoring event with zero datapoints")

        else:
            pass
            #print("Ignoring Unclassified or unknown event %d" % event['id'])

        count = count + 1
        if count >= maxEvents:
            print("reached maxEvents (%d) - stopping" % maxEvents)
            break


    return eventLst
    
def getFname(userId):
    fname = 'user_%s_data.json' % userId
    return fname



def makeFalseAlarmSummary(userId,configFname, download=False, maxEvents=10000):
    fname = getFname(userId)
    if download:
        eventLst = downloadData(userId,configFname, maxEvents=maxEvents)
        seizureFile = open(fname, 'w')
        seizureFile.write(json.dumps(eventLst, indent=2))
        seizureFile.close()
        print("data saved to %s" % fname)
    else:
        seizureFile = open(fname, 'r')
        eventLst = json.load(seizureFile)
        seizureFile.close()
        

    print("Loaded %d Events" % len(eventLst))

    #Now summarise the data by loading it into a pandas dataframe.
    df = pd.DataFrame(eventLst)
    df['dataTime'] = pd.to_datetime(df['dataTimeStr'])


    # False Alarms
    dfSummary = df.query('osdAlarmState!=1').groupby([
        df['userId'],
        df['dataTime'].dt.floor('d'),
        df['type'],
        df['osdAlarmState']
    ]).size()
    print("Alarms")
    print(dfSummary)
    print()

    # Warnings
    dfSummary = df.groupby([
        df['userId'],
        pd.Grouper(key='dataTime', freq='W-MON'),
        #df['dataTime'].dt.floor('W'),
        df['type'],
        df['osdAlarmState']
    ]).size()
    print("Warnings")
    print(dfSummary)
    
        
    return

    
    templateDir = os.path.join(os.path.dirname(__file__), 'templates/')
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(
            templateDir
        ))

    # Render page
    template = env.get_template('index.html.template')
    outFilePath = os.path.join(outDir,'index.html')
    outfile = open(outFilePath, 'w')
    dataTime = dateutil.parser.parse(analyser.eventObj['dataTime'])
    pageData={
        'eventId': analyser.eventObj['id'],
        'userId': analyser.eventObj['userId'],
        'eventDate': dataTime.strftime("%Y-%m-%d %H:%M"),
        'osdAlarmState': analyser.eventObj['osdAlarmState'],
        'eventType': analyser.eventObj['type'],
        'eventSubType': analyser.eventObj['subType'],
        'eventDesc': analyser.eventObj['desc'],
        'alarmFreqMin': dataObj['alarmFreqMin'],
        'alarmFreqMax': dataObj['alarmFreqMax'],
        'alarmThreshold': dataObj['alarmThresh'],
        'alarmRatioThreshold': dataObj['alarmRatioThresh'],
        'roiRatioMax': np.max(analyser.roiRatioLst),
        'roiRatioMaxThresholded': np.max(analyser.roiRatioThreshLst),
        'minRoiAlarmPower' : analyser.minRoiAlarmPower,
        'pageDateStr': (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M"),
        }
    print(pageData)
    outfile.write(template.render(data=pageData))
    outfile.close()

    # Plot Raw data graph
    analyser.plotRawDataGraph(os.path.join(outDir,'rawData.png'))

    # Plot Analysis data graph
    analyser.plotAnalysisGraph(os.path.join(outDir,'analysis.png'))

    # Plot Spectrum graph
    analyser.plotSpectrumGraph(os.path.join(outDir,'spectrum.png'))

    # Copy css and js into output directory.
    distutils.dir_util.copy_tree(os.path.join(templateDir,"js"),
                                 os.path.join(outDir,"js"))
    distutils.dir_util.copy_tree(os.path.join(templateDir,"css"),
                                 os.path.join(outDir,"css"))
    
    
    print("Data written to %s" % outFilePath)





if (__name__=="__main__"):
    print("makeFalseALarmSummary.py.main()")
    parser = argparse.ArgumentParser(description='analyse false alarms for a user')
    parser.add_argument('--config', default="credentials.json",
                        help='name of json file containing api login token')
    parser.add_argument('--user', default=None,
                        help='user ID number of user to be analysed')
    parser.add_argument('--download', action='store_true',
                        help="Download data from remote database rather than using local data")
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    #analyse_event(configFname=args['config'])


    if (args['user'] is not None):
            print("Analysing False Alarms for User %s" % args['user'])
            makeFalseAlarmSummary(args['user'],args['config'], download=args['download'])
    else:
        print("Not doing anything")
