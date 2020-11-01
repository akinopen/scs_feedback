from abc import abstractmethod
from enum import Enum

from django.conf import settings
from django.utils.module_loading import import_string

__all__ = ("BasePlatform", "Platform", "get_service")


class Platform(Enum):
    SLACK = "slack"


class BasePlatform:
    @abstractmethod
    def request_feedback(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def ask_feedback(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def give_feedback(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def send_feedback(self, *args, **kwargs):
        raise NotImplementedError


def get_service(platform: Platform):
    feedback_platform = settings.FEEDBACK_PLATFORMS[platform.value]
    service = import_string(feedback_platform["class"])
    return service(feedback_platform.get("settings", {}))
