#!/usr/bin/env python3

import datetime
import dateutil.parser
import os
import argparse
import json
# import tempfile
import jinja2
import numpy as np
import distutils.dir_util

import libosd.analyse_event
import libosd.webApiConnection



def makeEventSummary(eventId,configFname):
    analyser = libosd.analyse_event.EventAnalyser(configFname=args['config'])
    outDir = os.path.join("output","Event_%d_summary" % eventId)
    os.makedirs(outDir, exist_ok=True)
    print("makeEventSummary - outDir=%s" % outDir)
    

    inFile = open(configFname,'r')
    configObj = json.load(inFile)
    inFile.close()
    osd = libosd.webApiConnection.WebApiConnection(
        cfg=configFname,
        download=True,
        debug=False)
    eventObj = osd.getEvent(eventId, includeDatapoints=True)

    outFile = open(os.path.join(outDir,"rawData.json"),"w")
    json.dump(eventObj, outFile,sort_keys=True, indent=4)
    outFile.close()
    

    analyser.loadEvent(int(args['event']))

    print(analyser.eventObj)
    # Extract data from first datapoint to get OSD settings at time of event.
    dp=analyser.dataPointsObj[0]
    dpObj = json.loads(dp['dataJSON'])
    dataObj = json.loads(dpObj['dataJSON'])
    #print(dataObj)

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
        'alarmFreqMin': analyser.alarmFreqMin,
        'alarmFreqMax': analyser.alarmFreqMax,
        'alarmThreshold': analyser.alarmThresh,
        'alarmRatioThreshold': analyser.alarmRatioThresh,
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
    print("makeEventSummary.py.main()")
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


    if (args['event'] is not None):
        if (args['test'] is not None):
            print("Running Event Number %d on test server %s" %
                  (int(args['event']), args['test']))
            analyser.testEvent(int(args['event']), args['test'])
        else:
            print("Analysing Event Number %d" % int(args['event']))
            makeEventSummary(int(args['event']),args['config'])
    elif (args['list']):
        analyser.listEvents()
    else:
        print("Not doing anything")
