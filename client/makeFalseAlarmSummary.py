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


def getFalseAlarmDf(userId, credFname="client.cfg",
                    includeUnknowns=False,
                    download=False,
                    debug=False):
    osd = libosd.webApiConnection.WebApiConnection(cfg=credFname,
                                                   download=download,
                                                   debug=debug)
    if (userId=="all"):
        eventLst = osd.getEvents(userId=None, includeDatapoints=False)
    else:
        eventLst = osd.getEvents(userId=userId, includeDatapoints=False)

    print("Loaded %d Events" % len(eventLst))

    #Now summarise the data by loading it into a pandas dataframe.
    df = pd.DataFrame(eventLst)
    df = df.fillna('unclassified')
    df['dataTime'] = pd.to_datetime(df['dataTime'])
    # We need to rename column 'type' because 'type' is a python keyword
    df['eventType'] = df['type']
    df = df.drop('type', axis=1)
    #print(df[['id','userId','dataTime','osdAlarmState','eventType']])

    # False Alarms
    # Ignore warnings.   Include events explicitly tagge as false alarm
    if (includeUnknowns):
        queryStr = 'osdAlarmState!=1 and (eventType=="False Alarm" or eventType=="Unknown")'
    else:
        queryStr = 'osdAlarmState!=1 and (eventType=="False Alarm")'
    df = df.query(queryStr)
    df=df.query("not(desc.str.lower().str.contains('test'))")

    return(df)


def extractValue(keyStr, row):
    #print("extractValue - row=",row,type(row))
    if ('dataJSON' in row):
        #print("dataJSON=%s" % row['dataJSON'])
        try:
            dataObj = json.loads(row['dataJSON'])
            if (keyStr in dataObj.keys()):
                val = dataObj[keyStr]
                #print("Extracted %s" % str(val))
            else:
                #print("extractValue ERROR - %s is not in dataObj" % keyStr)
                val = None
        except json.JSONDecodeError:
            #print("decode Error")
            val = None
    else:
        #print("extractValue ERROR - dataJSON is not in row", row)
        val = None
    return val

def addOsdColumns(df):
    """adds some extra columns for the OSD algorithm to dataframe DF
    by querying the dataJSON string for each event.
    """
    df['alarmThresh'] = df.apply(lambda row: extractValue('alarmThresh',row), axis=1)
    df['alarmRatioThresh'] = df.apply(lambda row: extractValue('alarmRatioThresh',row), axis=1)
    df['phoneAppVersion'] = df.apply(lambda row: extractValue('phoneAppVersion',row), axis=1)
    df['watchAppVersion'] = df.apply(lambda row: extractValue('watchSdVersion',row), axis=1)

    #print(df)
    return df


def makeFalseAlarmSummary(userId, credentialsFname="client.cfg", download=False, maxEvents=10000, debug=False):
    columnLst = ['id','userId','dataTime','osdAlarmState','eventType','alarmThresh', 'alarmRatioThresh', 'phoneAppVersion', 'watchAppVersion', 'desc']
    df = getFalseAlarmDf(userId, credentialsFname,
                         includeUnknowns=False,
                         download=download,
                         debug=debug)
    df = addOsdColumns(df)
    print(df.columns)
    print(df[columnLst])
    df = getFalseAlarmDf(userId, credentialsFname,
                         includeUnknowns=True,
                         download=download,
                         debug=debug)
    df = addOsdColumns(df)
    print(df[columnLst])

    dfSummary = df.groupby([
        'userId',
        'alarmThresh',
        #df['userId'],
        pd.Grouper(key='dataTime', freq='W-MON'),
        #df['eventType'],
        #df['osdAlarmState']
    ]).size()
    print(dfSummary)
    print()

    
        
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
