from rest_framework import serializers
from django.utils import timezone

from users.serializers import UserSerializer
from .models import Event, EventRegistration


class EventReadSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()

    class Meta:
        model = Event
        fields = ["id", "title", "description", "date", "location", "organizer", "is_registration_active"]


class EventWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "location", "is_registration_active"]

    def create(self, validated_data):
        validated_data["organizer"] = self.context["request"].user
        event = super().create(validated_data)
        return event

    def validate(self, attrs):
        extra_fields = set(attrs.keys()) - set(self.Meta.fields)
        if extra_fields:
            raise serializers.ValidationError(f"Invalid fields: {', '.join(extra_fields)}")
        return attrs

    def validate_date(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("The event date must be in the future.")
        return value


class EventRegistrationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    event = EventReadSerializer()

    class Meta:
        model = EventRegistration
        fields = ["id", "user", "event", "registration_date"]
        read_only_fields = ["id", "user", "event", "registration_date"]
