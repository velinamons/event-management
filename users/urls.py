from django.urls import path
from .views import ListUsersView, RetrieveUserView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", ListUsersView.as_view(), name="user-list"),
    path("<int:pk>/", RetrieveUserView.as_view(), name="user-retrieve"),
]
