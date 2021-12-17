import json
import datetime
import numpy as np
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User

from datapoints.models import Datapoint
from datapoints.serializers import DatapointSerializer, DatapointSummarySerializer
from events.models import Event
from events.serializers import EventSerializer

UNVALIDATED_ALARM_TYPE = 0
UNVALIDATED_WARNING_TYPE = 1


class DatapointUploadCsv(APIView):
    def createEvent(self,eventType, dataTime):
        eventData = {
            'userId' : self.request.user.pk,
            'eventType' : eventType,
            'dataTime' : dataTime,
            'desc' : "Created from DatapointUploadCsv",
        }
        print("eventData=",eventData)
        serializer = EventSerializer(data=eventData)
        if serializer.is_valid():
            serializer.save()
    
    def post(self, request, format=None):
        #print("DatapointUploadCsv - data=%s" % request.data)
        #print("DatapointUploadCsv - user=%s" % str(self.request.user))
        print("%d lines uploaded" % len(request.data))
        lastStatus="OK"
        lastTime = None
        for lineStr in request.data:
            if len(lineStr)>0:
                #print("processing line %s" % lineStr)
                lineParts = lineStr.split(',')
                lineObj = {}
                lineObj['dateStr'] = lineParts[0]
                fftArr = []
                for n in range(0, 10):
                    fftArr.append(float(lineParts[n+1]))
                lineObj['fftArr'] = fftArr
                lineObj['specPower'] = float(lineParts[11])
                lineObj['roiPower'] = float(lineParts[12])
                lineObj['sampleFreq'] = float(lineParts[13])
                lineObj['statusStr'] = lineParts[14].strip()
                lineObj['hr'] = float(lineParts[15])
                rawDataArr = []
                for n in range(16, len(lineParts)):
                    rawDataArr.append(float(lineParts[n]))
                lineObj['rawData'] = rawDataArr

                jsonStr = json.dumps(lineObj)
                #print(jsonStr)

                # 04-11-2019 00:00:01
                dataDate = datetime.datetime.strptime(
                    lineObj['dateStr'],
                    "%d-%m-%Y %H:%M:%S"
                )
                dataDateStr = dataDate.strftime("%Y-%m-%d %H:%M:%S")
                dpData = {
                    "dataTime": dataDateStr,
                    "userId": self.request.user.pk,
                    "statusStr": lineObj['statusStr'],
                    "accMean": np.mean(lineObj['rawData']),
                    "accSd": np.std(lineObj['rawData']),
                    "hr": lineObj['hr'],
                    "categoryId": 0,
                    "eventId": 0,
                    "dataJSON": json.dumps(lineObj),
                }
        
                serializer = DatapointSerializer(data=dpData)
                if serializer.is_valid():
                    serializer.save()
                    # Create an event if appropriate
                    if (lastStatus=="ALARM" and lineObj['statusStr']!="ALARM"):
                        print("Creating alarm event",dpData)
                        self.createEvent(
                            UNVALIDATED_ALARM_TYPE,
                            dpData['dataTime'])
                    if (lastStatus=="WARNING" and lineObj['statusStr']!="ALARM"):
                        print("Creating warning event",dpData)
                        self.createEvent(
                            UNVALIDATED_WARNING_TYPE,
                            dpData['dataTime'])
                    lastStatus = lineObj['statusStr']
                    lastTime = dataDateStr
                else:
                    return Response(
                        serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                pass
                #print("skipping empty line")
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class DatapointList(generics.ListCreateAPIView):
    serializer_class = DatapointSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    queryset = Datapoint.objects.all()


class DatapointSummaryList(generics.ListAPIView):
    """
    Returns summarised data for each datapoint 
    (does not include the rawdata array)
    """
    serializer_class = DatapointSummarySerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    #queryset = Datapoint.objects.all()

    def get_queryset(self):
        """
        gets a filtered dataset based on query parameters:
           user : required userId
           start : start date/time yyyy-mm-dd hh:mm:ss
           end : end date/time yyyy-mm-dd hh:mm:ss
           duration:  required duration (minutes)
        If both start and end are specified, duration is ignored.
        duration is used if only start or end is specified.
        """
        queryset = Datapoint.objects.all().order_by('dataTime')
        user = self.request.query_params.get('user', None)
        startDateStr = self.request.query_params.get('start', None)
        endDateStr = self.request.query_params.get('end', None)
        durationMinStr = self.request.query_params.get('duration', None)

        # convert dates into datetime objects.
        if startDateStr is not None:
            startDate = datetime.datetime.strptime(
                    startDateStr, "%Y-%m-%d %H:%M:%S")
        else:
            startDate = None

        if endDateStr is not None:
            endDate = datetime.datetime.strptime(
                    endDateStr, "%Y-%m-%d %H:%M:%S")
        else:
            endDate = None

        # Decide which start and end date to use, based on which parameters
        # we have been given.
        if (startDate is None and endDate is None):
            print("no dates specified - returning all records")
        else:
            if (startDate is None):
                print("startDate not specified - trying to derive it from endDate")
                if (durationMinStr is not None):
                    dt = datetime.timedelta(minutes=float(durationMinStr))
                    startDate = endDate-dt
                else:
                    print("duration not specified, so we can't!")
                    startDate = None
                    endDate = None
            if (endDate is None):
                print("endDate not specified - trying to derive it from endDate")
                if (durationMinStr is not None):
                    dt = datetime.timedelta(minutes=float(durationMinStr))
                    endDate = startDate+dt
                else:
                    print("duration not specified, so we can't!")
                    startDate = None
                    endDate = None
            
            
        print("DatapointSummaryList.get_queryset() - user=%s, start=%s, end=%s, duration=%s" % (user,startDateStr, endDateStr, durationMinStr))
        print("DatapointSummaryList.get_queryset() - user=%s, start=%s, end=%s, duration=%s" % (
            user,
            startDate.strftime("%Y-%m-%d %H:%M:%S"),
            endDate.strftime("%Y-%m-%d %H:%M:%S"),
            durationMinStr))

        if user is not None:
            queryset = queryset.filter(userId=user)
        if startDate is not None and endDate is not None:
            queryset = queryset.filter(dataTime__gte=startDate, dataTime__lte=endDate)
        return queryset

    
    
class DatapointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer
    permission_classes = (
        #permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
        #IsOwnerOrReadOnly
        #IsOwnerOrFail,
    )


