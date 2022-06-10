#!/usr/bin/python3

import argparse

import libosd.webApiConnection
import libosd.loadConfig


def listEvents(userId, credentialsFname="client.cfg", seizure=False,
               download=False, maxEvents=10000, debug=False):
    osd = libosd.webApiConnection.WebApiConnection(cfg=credentialsFname,
                                                   download=download,
                                                   debug=debug)
    if (userId == "all"):
        eventLst = osd.getEvents(userId=None, includeDatapoints=False)
    else:
        eventLst = osd.getEvents(userId=userId, includeDatapoints=False)

    print("Loaded %d Events" % len(eventLst))

    for eventObj in eventLst:
        if (not seizure
            or eventObj['type'] == "Seizure"):
            print("userId=%d, eventId=%d, date=%s, osdState=%d, "
                  "type=%s, subType=%s, notes=%s" %
                  (eventObj['userId'],
                   eventObj['id'],
                   eventObj['dataTime'],
                   eventObj['osdAlarmState'],
                   eventObj['type'],
                   eventObj['subType'],
                   eventObj['desc']))
    return


if (__name__=="__main__"):
    print("listEvents.py.main()")
    parser = argparse.ArgumentParser(description='List events in the database or local cache')
    parser.add_argument('--config', default="client.cfg",
                        help='name of json file containing configuration information and login credientials - see client.cfg.template')
    parser.add_argument('--user', default=None,
                        help='user ID number of user to be analysed')
    parser.add_argument('--download', action='store_true',
                        help="Download data from remote database rather than using local data")
    parser.add_argument('--debug', action='store_true',
                        help="Write debugging information to screen")
    parser.add_argument('--seizure', action='store_true',
                        help="List only seizure events")
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    print("Analysing False Alarms for User %s" % args['user'])
    listEvents(args['user'], args['config'], seizure=args['seizure'],
               download=args['download'], debug=args['debug'])
