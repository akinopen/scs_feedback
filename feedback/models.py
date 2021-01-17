from django.db import models
from django.utils.translation import gettext_lazy as _

from scs_feedback.utils import ChoicesEnum

__all__ = ("Feedback", "Request", "User")


class User(models.Model):
    team_id = models.CharField(_("Team Id"), max_length=50)
    user_id = models.CharField(_("User Id"), max_length=50)
    username = models.CharField(_("Username"), max_length=255, blank=True, null=True)
    full_name = models.CharField(_("Full name"), max_length=255, blank=True, null=True)
    avatar = models.URLField(_("Avatar"), blank=True, null=True)
    email = models.EmailField(_("Email"), blank=True, null=True)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.full_name or self.username or self.email or self.user_id


class Request(models.Model):
    class Status(ChoicesEnum):
        PENDING = "pending", _("Pending")
        IGNORED = "ignored", _("Ignored")
        REPLIED = "replied", _("Replied")

    sender = models.ForeignKey(
        User,
        related_name="requests",
        on_delete=models.CASCADE,
        verbose_name=_("Request by"),
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_requests",
        verbose_name=_("Requested from"),
    )
    message = models.TextField(_("Message"), blank=True, null=True)
    status = models.CharField(
        _("Status"),
        max_length=15,
        choices=Status.choices(),
        default=Status.PENDING.value,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Request")
        verbose_name_plural = _("Requests")

    def __str__(self):
        return f"FeedbackRequest #{self.id}"


class Feedback(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Author"),
        related_name="sent_feedbacks",
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Recipient"),
        related_name="received_feedbacks",
    )
    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        verbose_name=_("Feedback Request"),
        related_name="feedbacks",
        blank=True,
        null=True,
    )
    start_doing = models.TextField(_("Start doing"))
    continue_doing = models.TextField(_("Continue doing"))
    stop_doing = models.TextField(_("Stop doing"))
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Feedback")
        verbose_name_plural = _("Feedbacks")

    def __str__(self):
        return f"{self.author} -> {self.recipient}"
