from emails.enums import EmailType
from emails.email_builders.event_registration import EventRegistrationBuilder
from emails.email_builders.event_registration_canceled import EventRegistrationCanceledBuilder


def get_email_builder(email_type: EmailType, registration):
    builders = {
        EmailType.EVENT_REGISTRATION: EventRegistrationBuilder,
        EmailType.EVENT_REGISTRATION_CANCELED: EventRegistrationCanceledBuilder,
    }

    builder_cls = builders.get(email_type)
    if not builder_cls:
        raise ValueError(f"No email builder found for type: {email_type}")
    return builder_cls(registration)
