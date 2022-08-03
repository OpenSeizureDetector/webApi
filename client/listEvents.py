#!/usr/bin/env python3

import argparse
import pandas as pd
import json
import tabulate

import libosd.webApiConnection
import libosd.loadConfig


def listEvents(userId, credentialsFname="client.cfg", seizure=False,
               tc=False, unique=False,
               download=False, maxEvents=10000, debug=False):
    osd = libosd.webApiConnection.WebApiConnection(cfg=credentialsFname,
                                                   download=download,
                                                   debug=debug)
    if (userId == "all"):
        eventLst = osd.getEvents(userId=None, includeDatapoints=False)
    else:
        eventLst = osd.getEvents(userId=userId, includeDatapoints=False)

    print("Loaded %d Events" % len(eventLst))

    if (unique):
        # In this section we try to produce a list of unique events.
        # We select all events that are either
        #    - marked as a seizure
        #    - not an OSD warning (because we don't consisder warnings false alarms
        #    - does not include the word 'test' in the description.
        # We then group them by user ID and by time - all events within a 10 minute period are
        #  considered a single event rather than multiple seizures or false alarms.
        # We then select the 'best' event from within the group and add that to the list.  The
        #   'best' event is one that either
        #    - contains a text description
        #    - is a manual alarm
        #    - Otherwise the middle event in the time period is used.
        #print(eventLst)

        # Read the event list into a pandas data frame.
        df = pd.read_json(json.dumps(eventLst))
        # drop the dataJSON column because we do not need it.
        df=df.drop('dataJSON', axis=1)
        # Filter out warnings (unless they are tagged as a seizure) and tests.
        df=df.query("type=='Seizure' or osdAlarmState!=1")
        df=df.query("not(desc.str.lower().str.contains('test'))")
        #print(df.columns)
        #print(df.dtypes)
        df['dataTime'] = pd.to_datetime(df['dataTime'])
        #print(df.describe())
        #print(df.dtypes)
        # Group the data by userID and time period
        groupedDf=df.groupby(['userId','type',pd.Grouper(key='dataTime', freq='10min')])
        allUniqueEventsDf = pd.DataFrame()
        tcUniqueEventsDf = pd.DataFrame()
        allSeizureUniqueEventsDf = pd.DataFrame()
        falseAlarmUniqueEventsDf = pd.DataFrame()
        unknownUniqueEventsDf = pd.DataFrame()
        #
        # This is to set the print order when we print the data frames
        columnList = ['id', 'userId','dataTime','type','subType','osdAlarmState','desc']
        # Loop through the grouped data
        for groupParts, group in groupedDf:
            userId, eventType, dataTime = groupParts
            print("UserId=%d, type=%s, dataTime=%s" % (userId, eventType,
                                                       dataTime.strftime('%Y-%m-%d %H:%M:%S')))
            #print(type(group))
            #print(group[columnList])
            taggedRows=group[group.desc.str.len()>0]
            if len(taggedRows.index)>0:
                #print("Tagged Rows:")
                #print(taggedRows[columnList])
                outputRows = taggedRows
            else:
                #print("No tagged rows")
                manualAlarmRows=group[group.osdAlarmState==5]
                if len(manualAlarmRows.index)>0:
                    #print("ManualAlarmRows:")
                    #print(manualAlarmRows[columnList])
                    outputRows = manualAlarmRows
                else:
                    #print("No manual alarm rows")
                    outputRows = group

            # Now just pick the middle row of the ouput rows list as the unique event.
            outputIndex = int(len(outputRows.index)/2)
            #print("len(outputRows)=%d, outputIndex=%d" % (len(outputRows), outputIndex))
            #print("UniqueEvent=")
            eventRow = outputRows.iloc[[outputIndex]]
            #print(eventRow[columnList])
            allUniqueEventsDf = allUniqueEventsDf.append(eventRow)


            if eventRow['type'].str.contains('Seizure').any():
                allSeizureUniqueEventsDf = allSeizureUniqueEventsDf.append(eventRow)
            if eventRow['subType'].str.contains('Tonic-Clonic').any():
                tcUniqueEventsDf = tcUniqueEventsDf.append(eventRow)
            if eventRow['type'].str.contains('False Alarm').any():
                falseAlarmUniqueEventsDf = falseAlarmUniqueEventsDf.append(eventRow)
            if eventRow['type'].str.contains('Unknown').any():
                unknownUniqueEventsDf = unknownUniqueEventsDf.append(eventRow)

            
        print("All Unique Events (%d):" % len(allUniqueEventsDf.index))
        #print(tabulate(df, headers='keys', tablefmt='fancy_grid'))
        print(tabulate.tabulate(allUniqueEventsDf[columnList], headers=columnList, tablefmt='fancy_grid'))

        print()
        print("Unique Unknown Events (%d):" % len(unknownUniqueEventsDf.index))
        print(tabulate.tabulate(unknownUniqueEventsDf[columnList], headers=columnList, tablefmt='fancy_grid'))


        print()
        print("Unique False Alarm Events (%d):" % len(falseAlarmUniqueEventsDf.index))
        print(tabulate.tabulate(falseAlarmUniqueEventsDf[columnList], headers=columnList, tablefmt='fancy_grid'))

        
        print()
        print("Unique Seizure Events (%d):" % len(allSeizureUniqueEventsDf.index))
        print(tabulate.tabulate(allSeizureUniqueEventsDf[columnList], headers=columnList, tablefmt='fancy_grid'))

        print()
        print("Unique TC Seizure Events (%d):" % len(tcUniqueEventsDf.index))
        print(tabulate.tabulate(tcUniqueEventsDf[columnList], headers=columnList, tablefmt='fancy_grid'))

        #print(tcUniqueEventsDf, tcUniqueEventsDf.columns)
    else:
        for eventObj in eventLst:
            if (not seizure
                or eventObj['type'] == "Seizure"):
                if (not tc
                    or eventObj['subType'] == "Tonic-Clonic"):
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
    parser.add_argument('--nodownload', action='store_true',
                        help="Do not Download data from remote database - use local data instead")
    parser.add_argument('--debug', action='store_true',
                        help="Write debugging information to screen")
    parser.add_argument('--seizure', action='store_true',
                        help="List only seizure events")
    parser.add_argument('--tc', action='store_true',
                        help="List only tonic-clonic seizure events")
    parser.add_argument('--unique',action='store_true', help='List only unique events (events from the same user within 5 minutes are assumed to be part of the same event')
    argsNamespace = parser.parse_args()
    args = vars(argsNamespace)
    print(args)

    print("Analysing False Alarms for User %s" % args['user'])
    listEvents(args['user'], args['config'],
               seizure=args['seizure'], tc=args['tc'], unique=args['unique'],
               download=not args['nodownload'], debug=args['debug'])
