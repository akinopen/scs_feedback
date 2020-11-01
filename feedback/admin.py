from django.contrib import admin

from feedback.models import Feedback, Request

__all__ = ("FeedbackAdmin", "RequestAdmin")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    pass
