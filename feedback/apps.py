from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ("FeedbackConfig",)


class FeedbackConfig(AppConfig):
    name = "feedback"
    verbose_name = _("Feedback")
