from enum import Enum


class EmailType(str, Enum):
    EVENT_REGISTRATION = "event_registration"
    EVENT_REGISTRATION_CANCELED = "event_registration_canceled"
