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




def makeFalseAlarmSummary(userId,configFname):
    configObj = libosd.loadConfig.loadConfig(configFname)
    outDir = os.path.join("output","False_alarm_summary_user_%d" % userId)
    os.makedirs(outDir, exist_ok=True)
    print("makeFalseAlarmSummary - outDir=%s" % outDir)

    osd = libosd.webApiConnection.WebApiConnection(cfg="client.cfg",
                                 uname=configObj["uname"],
                                 passwd=configObj["passwd"],
                                 debug=True)
    analyser = libosd.analyse_event.EventAnalyser(configFname=args['config'])

    eventsObj = osd.getEvents(userId=userId)
    seizureEventLst = []
    falseAlarmEventLst = []
    for event in eventsObj:
        if (event['type'] is not None and event['type'] != 'Unknown'):
            print("%5d %s %s %s %s" % (event['id'],
                                       event['dataTime'],
                                       event['type'],
                                       event['subType'],
                                       event['desc']
                                       ))
            analyser.loadEvent(event['id'])
            # Extract data from first datapoint to get OSD settings
            #     at time of event.
            dp=analyser.dataPointsObj[0]
            dpObj = json.loads(dp['dataJSON'])
            dataObj = json.loads(dpObj['dataJSON'])

            eventSummaryObj = {}
            eventSummaryObj['id'] = event['id']
            eventSummaryObj['dataTime'] = dateutil.parser.parse(
                analyser.eventObj['dataTime'])
            eventSummaryObj['dataTimeStr'] = eventSummaryObj['dataTime'].strftime("%Y-%m-%d %H:%M")
            eventSummaryObj['type'] = event['type']
            eventSummaryObj['subType'] = event['subType']
            eventSummaryObj['desc'] = event['desc']
            eventSummaryObj['maxRoiRatio'] = max(analyser.roiRatioLst)
            eventSummaryObj['minRoiAlarmPower'] = analyser.minRoiAlarmPower
            eventSummaryObj['alarmFreqMin'] = dataObj['alarmFreqMin']
            eventSummaryObj['alarmFreqMax'] = dataObj['alarmFreqMax']
            eventSummaryObj['alarmThreshold'] = dataObj['alarmThresh']
            eventSummaryObj['alarmRatioThreshold'] = dataObj['alarmRatioThresh']
                            
            if (event['type'] in ('Seizure', 'Manual Alarm')):
                print("Adding to Seizure List")
                seizureEventLst.append(eventSummaryObj)
            else:
                falseAlarmEventLst.append(eventSummaryObj)
        else:
            pass
            #print("Ignoring Unclassified or unknown event %d" % event['id'])

        print(seizureEventLst)


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
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    #analyse_event(configFname=args['config'])


    if (args['user'] is not None):
            print("Analysing False Alarms for User %d" % int(args['user']))
            makeFalseAlarmSummary(int(args['user']),args['config'])
    else:
        print("Not doing anything")
