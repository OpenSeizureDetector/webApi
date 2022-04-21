#!/usr/bin/python3

import argparse
import json
import libosd.analyse_event
import libosd.webApiConnection
import libosd.osdAppConnection
import sys
import dateutil.parser
import time

import matplotlib.pyplot as plt


        
            
if (__name__=="__main__"):
    print("eventanalyser.py.main()")
    parser = argparse.ArgumentParser(description='analyse event')
    parser.add_argument('--config', default="client.cfg",
                        help='name of json file containing api login token')
    parser.add_argument('--event', default=None,
                        help='ID Number of the event to analyse')
    parser.add_argument('--list', action="store_true",
                        help='List all events in the database')
    parser.add_argument('--test',
                        help='Address of Device running OpenSeizureDetector Ap for Testing')
    parser.add_argument('--debug', action="store_true",
                        help='Write debugging information to screen')
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    #analyse_event(configFname=args['config'])

    analyser = libosd.analyse_event.EventAnalyser(configFname=args['config'],
                                                  debug=args['debug'])

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

