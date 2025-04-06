from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import EventRegistration
from events.serializers import EventRegistrationSerializer
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ListUsersView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False, is_active=True)


class RetrieveUserView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False, is_active=True)


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class MyEventRegistrationsView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventRegistrationSerializer

    def get_queryset(self):
        return EventRegistration.objects.filter(user=self.request.user).select_related("event", "user")
