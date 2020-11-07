from django.contrib import admin

from feedback.models import Feedback, Request

__all__ = ("FeedbackAdmin", "RequestAdmin")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    exclude = ("start_doing", "continue_doing", "stop_doing")
    list_display = ("author", "recipient", "created_at")
    list_filter = ("created_at",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "created_at")
    list_filter = ("created_at",)
    readonly_fields = ("sender", "recipients")
