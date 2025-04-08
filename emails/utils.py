from datetime import datetime
from functools import lru_cache
from typing import Any, Dict
import pytz

from core.settings import TIME_ZONE
from events.models import EventRegistration


@lru_cache
def get_timezone(tz_str: str) -> pytz.BaseTzInfo:
    return pytz.timezone(tz_str)


def get_gmt_offset_string(local_dt: datetime) -> str:
    offset = local_dt.utcoffset()
    offset_hours = offset.total_seconds() / 3600 if offset else 0
    sign = "+" if offset_hours >= 0 else "-"
    return f"GMT{sign}{int(abs(offset_hours))}"


def format_date_components(dt: datetime, tz_str: str = TIME_ZONE) -> Dict[str, str]:
    tz = get_timezone(tz_str)
    local_dt = dt.astimezone(tz)

    return {
        "date": local_dt.strftime(f"%B %d, %Y"),
        "time": local_dt.strftime(f"%H:%M"),
        "gmt_offset": get_gmt_offset_string(local_dt),
    }


def get_email_context(registration: EventRegistration) -> Dict[str, Any]:
    user = registration.user
    event = registration.event
    organizer = event.organizer

    event_components = format_date_components(event.date)
    registration_components = format_date_components(registration.registration_date)

    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "event_title": event.title,
        "event_description": event.description,
        "location": event.location,
        "organizer_name": organizer.first_name,
        "organizer_surname": organizer.last_name,
        "organizer_email": organizer.email,
        "event_date": event_components["date"],
        "event_time": event_components["time"],
        "event_timezone": event_components["gmt_offset"],
        "registration_date": registration_components["date"],
        "registration_time": registration_components["time"],
        "registration_timezone": registration_components["gmt_offset"],
    }
