from django.urls import path
from .views import EventRetrieveUpdateDestroyView, EventListCreateView, EventRegisterView, EventUnregisterView

urlpatterns = [
    path("", EventListCreateView.as_view(), name="event-list-create"),
    path("<int:pk>/", EventRetrieveUpdateDestroyView.as_view(), name="event-ret-upd-del"),
    path("<int:pk>/register/", EventRegisterView.as_view(), name="event-register"),
    path("<int:pk>/unregister/", EventUnregisterView.as_view(), name="event-unregister"),
]
