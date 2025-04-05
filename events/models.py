from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="organized_events")
    is_registration_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.date}"
