from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from emails.enums import EmailType
from emails.email_builders import get_email_builder
from events.models import EventRegistration


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email(self, registration_id: int, email_type: EmailType) -> None:
    from_email = None
    try:
        registration = EventRegistration.objects.select_related("event", "user", "event__organizer").get(id=registration_id)
        builder = get_email_builder(email_type, registration)

        subject = builder.get_subject()
        html_content = builder.get_html_content()
        text_content = builder.get_text_content()

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[registration.user.email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    except Exception as exc:
        raise self.retry(exc=exc)
