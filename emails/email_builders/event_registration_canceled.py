from django.template.loader import render_to_string
from emails.email_builders.base import BaseEmailBuilder
from emails import utils


class EventRegistrationCanceledBuilder(BaseEmailBuilder):
    def get_subject(self) -> str:
        return f"❌ {self.registration.event.title}: {self.registration.user.username} registration canceled"

    def get_html_content(self) -> str:
        context = self._get_context()
        return render_to_string("emails/event_registration_canceled.html", context)

    def get_text_content(self) -> str:
        context = self._get_context()
        return render_to_string("emails/event_registration_canceled.txt", context)

    def _get_context(self) -> dict:
        return utils.get_email_context(self.registration)
