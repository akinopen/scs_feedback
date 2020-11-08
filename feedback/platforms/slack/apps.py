from django.apps import AppConfig

__all__ = ("SlackConfig",)


class SlackConfig(AppConfig):
    name = "feedback.platforms.slack"
    verbose_name = "Slack"
