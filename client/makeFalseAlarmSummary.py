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

import libosd.webApiConnection
import libosd.loadConfig

import pandas as pd


    
def getFname(userId):
    fname = 'user_%s_data.json' % userId
    return fname



def makeFalseAlarmSummary(userId, credentialsFname="client.cfg", download=False, maxEvents=10000, debug=False):
    osd = libosd.webApiConnection.WebApiConnection(cfg=credentialsFname,
                                                   download=download,
                                                   debug=debug)
    if (userId=="all"):
        eventLst = osd.getEvents(userId=None, includeDatapoints=True)
    else:
        eventLst = osd.getEvents(userId=userId, includeDatapoints=True)

    print("Loaded %d Events" % len(eventLst))

    #Now summarise the data by loading it into a pandas dataframe.
    df = pd.DataFrame(eventLst)
    df = df.fillna('unclassified')
    df['dataTime'] = pd.to_datetime(df['dataTime'])
    print(df[['id','userId','dataTime','osdAlarmState','type']])

    # False Alarms
    dfSummary = df.query('osdAlarmState!=1').groupby([
        df['userId'],
        pd.Grouper(key='dataTime', freq='W-MON'),
        #df['dataTime'].dt.floor('d'),
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
    parser.add_argument('--config', default="client.cfg",
                        help='name of json file containing configuration information and login credientials - see client.cfg.template')
    parser.add_argument('--user', default=None,
                        help='user ID number of user to be analysed')
    parser.add_argument('--download', action='store_true',
                        help="Download data from remote database rather than using local data")
    parser.add_argument('--debug', action='store_true',
                        help="Write debugging information to screen")
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    #analyse_event(configFname=args['config'])


    if (args['user'] is not None):
            print("Analysing False Alarms for User %s" % args['user'])
            makeFalseAlarmSummary(args['user'],args['config'], download=args['download'], debug=args['debug'])
    else:
        print("Not doing anything")
