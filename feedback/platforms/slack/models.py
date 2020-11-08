from django.db import models
from django.utils.translation import gettext_lazy as _

__all__ = ("Team",)


class Team(models.Model):
    id = models.CharField(_("Id"), max_length=32, primary_key=True)
    name = models.CharField(_("Name"), max_length=32)
    bot_token = models.CharField(_("Bot Token"), max_length=64)

    class Meta:
        verbose_name = _("Slack Team")
        verbose_name_plural = _("Slack Teams")

    def __str__(self):
        return self.name
