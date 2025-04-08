from django.urls import path
from .views import ListUsersView, RetrieveUserView, RegisterView, MyEventRegistrationsView, MeView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("", ListUsersView.as_view(), name="user-list"),
    path("<int:pk>/", RetrieveUserView.as_view(), name="user-retrieve"),
    path("me/", MeView.as_view(), name="me"),
    path("me/registrations/", MyEventRegistrationsView.as_view(), name="my-registrations"),
]
