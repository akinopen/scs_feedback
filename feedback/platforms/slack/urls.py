from django.urls import path

from feedback.platforms.slack.views import GiveFeedback, Interaction, RequestFeedback

urlpatterns = [
    path("give/", GiveFeedback.as_view()),
    path("request/", RequestFeedback.as_view()),
    path("interaction/", Interaction.as_view()),
]
