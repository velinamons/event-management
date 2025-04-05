from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class RegisterView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ListUsersView(ListAPIView):
    queryset = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class RetrieveUserView(RetrieveAPIView):
    queryset = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
