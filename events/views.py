# events/views.py

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .models import Event
from .serializers import EventReadSerializer, EventWriteSerializer


class EventListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.all()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return EventWriteSerializer
        return EventReadSerializer

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class EventRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return EventWriteSerializer
        return EventReadSerializer

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ["PUT", "PATCH", "DELETE"] and obj.organizer != self.request.user:
            raise PermissionDenied("You are not the organizer of this event.")
        return obj
