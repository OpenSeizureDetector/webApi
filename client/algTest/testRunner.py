#!/usr/bin/python3

import argparse
import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import libosd.analyse_event
import libosd.webApiConnection


def runTest(configObj, debug=False):
    print("runTest - configObj="+json.dumps(configObj))
    osd = libosd.webApiConnection.WebApiConnection(
        cfg=configObj['credentialsFname'],
        download=configObj['download'],
        debug=debug)

    
    for eventId in configObj['eventsList']:
        print("Analysing event %s" % eventId)


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
