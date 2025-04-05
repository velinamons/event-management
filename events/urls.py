from django.urls import path
from .views import EventRetrieveUpdateDestroyView, EventListCreateView

urlpatterns = [
    path("", EventListCreateView.as_view(), name="event-list-create"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-ret-upd-del"),
]
