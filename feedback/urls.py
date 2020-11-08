from django.urls import include, path

urlpatterns = [
    path("slack/", include("feedback.platforms.slack.urls", namespace="slack")),
]
