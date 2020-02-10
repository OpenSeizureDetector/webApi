import json
from rest_framework import viewsets
from rest_framework import permissions
from events.models import Event
from events.serializers import EventSerializer
import common.queryUtils

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('dataTime')
    serializer_class = EventSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("EventViewSet.perform_create()")
        serializer.save(userId=self.request.user)


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
        queryset = Event.objects.all().order_by('dataTime')
        user = self.request.query_params.get('user', None)
        startDateStr = self.request.query_params.get('start', None)
        endDateStr = self.request.query_params.get('end', None)
        durationMinStr = self.request.query_params.get('duration', None)
        authUser = self.request.user
        print("events.views.get_queryset(): authUser="+str(authUser))

        queryset = common.queryUtils.dateFilter(
            queryset,
            startDateStr,
            endDateStr,
            durationMinStr)

        queryset = common.queryUtils.userFilter(
            queryset,
            user, authUser)
        return queryset

