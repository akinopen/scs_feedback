from django.urls import path

from feedback.platforms.slack.views import (
    CompleteSetup,
    GiveFeedback,
    Interaction,
    RequestFeedback,
    Setup,
)

app_name = "slack"

urlpatterns = [
    path("give/", GiveFeedback.as_view()),
    path("request/", RequestFeedback.as_view()),
    path("interaction/", Interaction.as_view()),
    path("setup/", Setup.as_view(), name="setup"),
    path("setup/complete/", CompleteSetup.as_view(), name="setup-complete"),
]
