from django.contrib import admin

from feedback.platforms.slack.models import Team

__all__ = ("TeamAdmin",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    exclude = ("bot_token",)

    def has_change_permission(self, request, obj=None):
        return False
