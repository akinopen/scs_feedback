import json

from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from feedback.platforms import Platform, get_service

__all__ = ("GiveFeedback", "Interaction", "RequestFeedback")


@method_decorator(csrf_exempt, name="dispatch")
class GiveFeedback(View):
    service = get_service(Platform.SLACK)

    def post(self, request: HttpRequest) -> HttpResponse:
        # noinspection PyTypeChecker
        trigger_id = request.POST["trigger_id"]
        self.service.give_feedback(trigger_id)
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
        trigger_id = request.POST["trigger_id"]
        self.service.request_feedback(trigger_id)
        return HttpResponse()
