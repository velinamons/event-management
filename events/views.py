from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from emails.enums import EmailType
from .filters import EventFilter
from .models import Event, EventRegistration
from .serializers import EventReadSerializer, EventWriteSerializer, EventRegistrationSerializer
from emails import tasks


class EventListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.all().select_related("organizer").order_by("-is_registration_active", "date")

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


class EventRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found."}, status=status.HTTP_404_NOT_FOUND)

        if not event.is_registration_active:
            return Response({"detail": "Registration is closed for this event."}, status=status.HTTP_400_BAD_REQUEST)

        if event.organizer == request.user:
            return Response({"detail": "Organizers cannot register for their own events."},
                            status=status.HTTP_400_BAD_REQUEST)

        if EventRegistration.objects.filter(user=request.user, event=event).exists():
            return Response({"detail": "You are already registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        registration = EventRegistration.objects.create(user=request.user, event=event)

        tasks.send_email.delay(registration_id=registration.id, email_type=EmailType.EVENT_REGISTRATION)

        serializer = EventRegistrationSerializer(registration)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class EventUnregisterView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            registration = EventRegistration.objects.get(user=request.user, event_id=pk)
        except EventRegistration.DoesNotExist:
            return Response({"detail": "You are not registered for this event."}, status=status.HTTP_400_BAD_REQUEST)

        tasks.send_email.delay(registration_id=registration.id, email_type=EmailType.EVENT_REGISTRATION_CANCELED)

        registration.delete()
        return Response({"detail": "Successfully unregistered."}, status=status.HTTP_204_NO_CONTENT)
