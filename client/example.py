#!/usr/bin/python3

import json
import libosd
# Note, in test DB graham4 is a staff (researcher) user
#              and graham29 is a normal user

for unameStr in ("graham29","graham4"):
    print("**********************")
    print("Trying as user %s" % unameStr)
    print("**********************")
    osd = libosd.libosd(cfg="client.cfg", uname=unameStr,
                        passwd="testpwd1", debug=True)
    eventsObj = osd.getEvents(userId=38)
    if (eventsObj is not None):
        for event in eventsObj:
            print(event)
    else:
        print("ERROR - No Data Returned");

    datapointsObj = osd.getDataPointsByEvent(eventId=395)
    if (datapointsObj is not None):
        for dp in datapointsObj:
            #print("dp=",dp)
            dpObj = json.loads(dp['dataJSON'])
            dataObj = json.loads(dpObj['dataJSON'])
            #print(dataObj.keys())
            print("%s, %d, %d, %.0f, %.0f, %.2f" % (dataObj['dataTime'],
                                              dp['id'], dp['eventId'],
                                              dataObj['specPower'],dataObj['roiPower'],
                                              dataObj['roiPower']/dataObj['specPower']                                      ))
    else:
        print("ERROR - No Data Returned")

    
