#!/usr/bin/python3

import argparse
import json
import sys
import os
import importlib
import dateutil.parser
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import libosd.analyse_event
import libosd.webApiConnection

def dateStr2secs(dateStr):
    ''' Convert a string representation of date/time into seconds from
    the start of 1970 (standard unix timestamp)
    '''
    parsed_t = dateutil.parser.parse(dateStr)
    return parsed_t.timestamp()


def dp2rawData(dp):
    '''Accepts a dataPoint object from the osd Database and converts it into
    a 'raw data' JSON string that would have been received by the phone to
    create it.
    This is useful to reproduce the exact phone behaviour from datapoints
    stored in the database.
    '''
    currTs = dateStr2secs(dp['dataTime'])
    dpObj = json.loads(dp['dataJSON'])
    dataObj = json.loads(dpObj['dataJSON'])
    # Create raw data list
    accelLst = []
    # FIXME:  It is not good to hard code the length of an array!
    for n in range(0,125):
        accelLst.append(dataObj['rawData'][n])

    rawDataObj = {"dataType": "raw", "Mute": 0}
    rawDataObj['HR'] = dataObj['hr']
    rawDataObj['data'] = accelLst
    # FIXME - add o2sat
    dataJSON = json.dumps(rawDataObj)
    return dataJSON


def runTest(configObj, debug=False):
    print("runTest - configObj="+json.dumps(configObj))
    osd = libosd.webApiConnection.WebApiConnection(
        cfg=configObj['credentialsFname'],
        download=configObj['download'],
        debug=debug)
    
    # Create an instance of the relevant Algorithm class for each algorithm
    # specified in the configuration file.
    # They are imported dynamically so we do not need to have 'import'
    # statements for all the possible algorithm classes in this file.
    algs = []
    algNames = []
    for algObj in configObj['algorithms']:
        print(algObj['name'])
        moduleId = algObj['alg'].split('.')[0]
        classId = algObj['alg'].split('.')[1]
        print("Importing Module %s" % moduleId)
        module = importlib.import_module(moduleId)

        settingsStr = json.dumps(algObj['settings'])
        print("settingsStr=%s (%s)" % (settingsStr, type(settingsStr)))
        algs.append(eval("module.%s(settingsStr)" % (classId)))
        algNames.append(algObj['name'])

    # Now we loop through each event in the eventsList and run the event
    # through each of the specified algorithms.
    # we collect statistics of the number of alarms and warnings generated
    # for each event for each algorithm.
    # result[e][a][s] is the count of the number of datapoints in event e giving status s using algorithm a.
    nEvents = len(configObj['eventsList'])
    nAlgs = len(algs)
    nStatus =5 # The number of possible OSD statuses 0=OK, 1=WARNING, 2=ALARM etc.
    #results = [[[0 for e in range(nEvents)] 0 for a in range(nAlgs)] 0 for s in range(nStaus)]
    results = np.zeros((nEvents, nAlgs, nStatus))
    for eventNo in range(0,nEvents):
        eventId = configObj['eventsList'][eventNo]
        print("Analysing event %s" % eventId)
        eventObj = osd.getEvent(eventId, includeDatapoints=True)
        print(eventObj.keys())
        for algNo in range(0, nAlgs):
            alg = algs[algNo]
            print("Processing Algorithm %d (%s): " % (algNo, alg.__class__.__name__))
            sys.stdout.write("Looping through Datapoints: ")
            for dp in eventObj['datapoints']:
                sys.stdout.write(".")
                sys.stdout.flush()
                retVal = alg.processDp(dp2rawData(dp))
                #print(alg.__class__.__name__, retVal)
                retObj = json.loads(retVal)
                statusVal = retObj['alarmState']
                results[eventNo][algNo][statusVal] += 1
            sys.stdout.write("\n")
            sys.stdout.flush()
    print(results)


    lineStr = "eventId, type, subType, "
    for algNo in range(0,nAlgs):
        lineStr = "%s, %s" % (lineStr, algNames[algNo])
    lineStr = "%s, desc" % lineStr
    print(lineStr)
    
    for eventNo in range(0,nEvents):
        eventId = configObj['eventsList'][eventNo]
        eventObj = osd.getEvent(eventId, includeDatapoints=False)
        lineStr = "%s, %s, %s" % (eventId, eventObj['type'], eventObj['subType'])
        for algNo in range(0,nAlgs):
            if results[eventNo][algNo][2] > 0:
                lineStr = "%s, ALARM" % (lineStr)
            elif results[eventNo][algNo][1] > 0:
                lineStr = "%s, WARN" % (lineStr)
            else:
                lineStr = "%s, ----" % (lineStr) 
        lineStr = "%s, %s" % (lineStr, eventObj['desc'])
        print(lineStr)
        
def main():
    print("testRunner.main()")
    parser = argparse.ArgumentParser(description='Seizure Detection Test Runner')
    parser.add_argument('--config', default="testConfig.json",
                        help='name of json file containing test configuration')
    parser.add_argument('--debug', action="store_true",
                        help='Write debugging information to screen')
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)


    inFile = open(args['config'],'r')
    configObj = json.load(inFile)
    inFile.close()
    runTest(configObj, args['debug'])
    


if __name__ == "__main__":
    main()
