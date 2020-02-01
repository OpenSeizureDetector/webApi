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
from datapoints.serializers import DatapointSerializer


class DatapointUploadCsv(APIView):
    def post(self, request, format=None):
        #print("DatapointUploadCsv - data=%s" % request.data)
        #print("DatapointUploadCsv - user=%s" % str(self.request.user))
        #dataLines = request.data.split('\n')
        print("%d lines uploaded" % len(request.data))
        for lineStr in request.data:
            # print("line is %d characters long" % len(lineStr))
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
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]


class DatapointDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Datapoint.objects.all()
    serializer_class = DatapointSerializer
    permission_classes = (
        #permissions.IsAuthenticatedOrReadOnly,
        permissions.IsAuthenticated,
        #IsOwnerOrReadOnly
        #IsOwnerOrFail,
    )


