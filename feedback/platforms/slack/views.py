import json

from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView

from feedback.platforms import Platform, get_service

__all__ = ("CompleteSetup", "GiveFeedback", "Interaction", "RequestFeedback", "Setup")


@method_decorator(csrf_exempt, name="dispatch")
class GiveFeedback(View):
    service = get_service(Platform.SLACK)

    def post(self, request: HttpRequest) -> HttpResponse:
        # noinspection PyTypeChecker
        team_id = request.POST["team_id"]
        trigger_id = request.POST["trigger_id"]
        self.service.give_feedback(team_id, trigger_id)
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class Interaction(View):
    service = get_service(Platform.SLACK)

    def post(self, request: HttpRequest) -> HttpResponse:
        # noinspection PyTypeChecker
        payload = json.loads(request.POST["payload"])
        self.service.handle_interaction(payload)
        return HttpResponse()


@method_decorator(csrf_exempt, name="dispatch")
class RequestFeedback(View):
    service = get_service(Platform.SLACK)

    def post(self, request: HttpRequest) -> HttpResponse:
        # noinspection PyTypeChecker
        team_id = request.POST["team_id"]
        trigger_id = request.POST["trigger_id"]
        self.service.request_feedback(team_id, trigger_id)
        return HttpResponse()


class Setup(RedirectView):
    service = get_service(Platform.SLACK)

    def get_redirect_url(self, *args, **kwargs):
        redirect_uri = self.request.build_absolute_uri(reverse("slack:setup-complete"))
        return self.service.oauth_service.get_authorization_url(redirect_uri)


class CompleteSetup(RedirectView):
    service = get_service(Platform.SLACK)
    url = "https://www.google.com"  # TODO: This is temporary

    def get(self, request, *args, **kwargs):
        self.service.register_team(self.request.GET["code"])
        return super(CompleteSetup, self).get(request, *args, **kwargs)
