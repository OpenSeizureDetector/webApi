from rest_framework import viewsets
from rest_framework import permissions
from events.models import Event
from events.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('dataTime')
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("EventViewSet.perform_create()")
        serializer.save(userId=self.request.user)
