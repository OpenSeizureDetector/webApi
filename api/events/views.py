import json
#from datetime import datetime, timedelta
import datetime

from rest_framework import viewsets
from rest_framework import permissions
from events.models import Event
from events.serializers import EventSerializer
import common.queryUtils


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('dataTime')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    # from: https://stackoverflow.com/questions/48319957/djangofilterbackend-field-null
    filter_fileds = {'type' : ['isnull']}

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
        # Build the date from 10 days ago to not retrieve by default all events since the account creation.
        current_datetime = datetime.datetime.now()
        date_minus_10_days = current_datetime - datetime.timedelta(days=10)
        formatted_start_date_by_default = date_minus_10_days.strftime("%Y-%m-%d %H:%M:%S")
        formatted_end_date_by_default = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        user = self.request.query_params.get('user', None)
        startDateStr = self.request.query_params.get('start', formatted_start_date_by_default)
        endDateStr = self.request.query_params.get('end', formatted_end_date_by_default)
        durationMinStr = self.request.query_params.get('duration', None)
        authUser = self.request.user
        print("events.views.get_queryset(): authUser="+str(authUser)+", startDateStr=%s, endDateStr=%s, durationMinStr=%s" % (startDateStr, endDateStr, durationMinStr))

        queryset = Event.objects.all().order_by('dataTime')

        queryset = common.queryUtils.dateFilter(
            queryset,
            startDateStr,
            endDateStr,
            durationMinStr)

        queryset = common.queryUtils.userFilter(
            queryset,
            user, authUser)
        return queryset

