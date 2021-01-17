import logging
from typing import Optional
from urllib.parse import urlencode

import requests
from slack import WebClient

from feedback.models import Feedback, Request, User
from feedback.platforms import BasePlatform
from feedback.platforms.slack.block_kit import Text
from feedback.platforms.slack.block_kit.blocks import Actions, Divider, Input, Section
from feedback.platforms.slack.block_kit.elements import (
    Button,
    MultiUsersSelect,
    PlainTextInput,
    UsersSelect,
)
from feedback.platforms.slack.models import Team
from feedback.platforms.slack.surfaces import Modal
from feedback.services import FeedbackService
from scs_feedback.utils import as_dict

__all__ = ("SlackService",)

logger = logging.getLogger(__name__)


class SlackService(BasePlatform):
    MODAL_TITLE = "Start/Continue/Stop"

    feedback_service = FeedbackService()

    def __init__(self, settings):
        self.oauth_service = SlackOAuthService(settings)

    def register_team(self, authorization_code: str) -> Team:
        response = self.oauth_service.get_access_token(authorization_code)
        if not response["ok"]:
            raise NotImplementedError(response)

        team, _ = Team.objects.get_or_create(
            id=response["team"]["id"],
            defaults={
                "name": response["team"]["name"],
                "bot_token": response["access_token"],
            },
        )
        return team

    def update_user_profile(self, user: User) -> User:
        info = self._get_client(user.team_id).users_info(user=user.user_id)
        if info["ok"]:
            user.username = info["user"].get("username", None)
            user.full_name = info["user"].get("real_name", None)
            user.email = info["user"].get("profile", {}).get("email", None)
            user.avatar = info["user"].get("profile", {}).get("image_512", None)
            user.save()

        return user

    def _get_client(self, team_id: str) -> WebClient:
        bot_token = Team.objects.get(id=team_id).bot_token
        return WebClient(token=bot_token)

    def request_feedback(self, team_id: str, trigger_id: str):
        modal: Modal = Modal(
            title=Text(type=Text.Type.PLAIN, text=self.MODAL_TITLE),
            submit=Text(type=Text.Type.PLAIN, text="Submit"),
            close=Text(type=Text.Type.PLAIN, text="Close"),
            blocks=[
                Input(
                    block_id="requestFrom",
                    label=Text(type=Text.Type.PLAIN, text="Request feedback from:"),
                    element=UsersSelect(
                        action_id="actionFrom",
                        placeholder=Text(type=Text.Type.PLAIN, text="Select user"),
                    ),
                ),
                Divider(),
                Input(
                    block_id="requestMessage",
                    label=Text(type=Text.Type.PLAIN, text="Message"),
                    optional=True,
                    element=PlainTextInput(action_id="actionMessage", multiline=True),
                ),
            ],
        )
        self._get_client(team_id).views_open(trigger_id=trigger_id, view=as_dict(modal))

    def ask_feedback(self, feedback_request: Request, user_id: str):
        text = f"<@{feedback_request.sender.user_id}> requested your feedback"
        self._get_client(feedback_request.sender.team_id).chat_postMessage(
            text=text,
            channel=user_id,
            blocks=as_dict(
                [
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=text,
                        ),
                    ),
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=f"*Message:* {feedback_request.message}",
                        ),
                    ),
                    Actions(
                        elements=[
                            Button(
                                action_id="give",
                                text=Text(type=Text.Type.PLAIN, text="Give now"),
                                style=Button.Style.PRIMARY,
                                value=str(feedback_request.id),
                            ),
                            Button(
                                action_id="ignore",
                                text=Text(type=Text.Type.PLAIN, text="Ignore"),
                                style=Button.Style.DANGER,
                                value=str(feedback_request.id),
                            ),
                        ],
                    ),
                ]
            ),
        )

    def give_feedback(
        self, team_id: str, trigger_id: str, request: Optional[Request] = None
    ):
        to_block = Input(
            block_id="giveTo",
            label=Text(type=Text.Type.PLAIN, text="Give feedback to:"),
            element=UsersSelect(
                action_id="actionTo",
                placeholder=Text(type=Text.Type.PLAIN, text="Select user"),
            ),
        )
        if request:
            to_block = Section(
                text=Text(
                    type=Text.Type.MARKDOWN,
                    text=f"You are giving feedback to <@{request.sender.user_id}>",
                ),
            )
        modal: Modal = Modal(
            title=Text(type=Text.Type.PLAIN, text=self.MODAL_TITLE),
            submit=Text(type=Text.Type.PLAIN, text="Submit"),
            close=Text(type=Text.Type.PLAIN, text="Close"),
            blocks=[
                to_block,
                Divider(),
                Input(
                    block_id="giveStart",
                    label=Text(type=Text.Type.PLAIN, text="Start doing"),
                    element=PlainTextInput(action_id="actionStart", multiline=True),
                ),
                Input(
                    block_id="giveContinue",
                    label=Text(type=Text.Type.PLAIN, text="Continue doing"),
                    element=PlainTextInput(action_id="actionContinue", multiline=True),
                ),
                Input(
                    block_id="giveStop",
                    label=Text(type=Text.Type.PLAIN, text="Stop doing"),
                    element=PlainTextInput(action_id="actionStop", multiline=True),
                ),
            ],
        )
        if request:
            modal.callback_id = str(request.id)
        self._get_client(team_id).views_open(trigger_id=trigger_id, view=as_dict(modal))

    def send_feedback(self, feedback: Feedback):
        text = f"New feedback from <@{feedback.author.user_id}>"
        self._get_client(feedback.author.team_id).chat_postMessage(
            text=text,
            channel=f"{feedback.recipient.user_id}",
            blocks=as_dict(
                [
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=text,
                        ),
                    ),
                    Divider(),
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=f"*Start doing:*\n{feedback.start_doing}",
                        ),
                    ),
                    Divider(),
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=f"*Continue doing:*\n{feedback.continue_doing}",
                        ),
                    ),
                    Divider(),
                    Section(
                        text=Text(
                            type=Text.Type.MARKDOWN,
                            text=f"*Stop doing:*\n{feedback.stop_doing}",
                        ),
                    ),
                ]
            ),
        )

    def ignore_request(self, feedback_request: Request, response_url: str):
        requests.post(
            response_url,
            json={
                "replace_original": True,
                "text": f"You ignored feedback request from <@{feedback_request.sender.user_id}>",
            },
        )

    def handle_interaction(self, payload: dict):
        if payload["type"] == "view_submission":
            values = payload["view"]["state"]["values"]
            if "requestFrom" in values:
                return self.handle_request_feedback(payload)
            elif "giveStart" in values:
                return self.handle_give_feedback(payload)
            else:
                logger.error(
                    f"Unhandled submission received: {payload['view']['state']}"
                )
        elif payload["type"] == "block_actions":
            actions = payload["actions"]
            for action in actions:
                if action["action_id"] == "give":
                    request = self.feedback_service.get_request(int(action["value"]))
                    self.give_feedback(
                        payload["team"]["id"], payload["trigger_id"], request
                    )
                elif action["action_id"] == "ignore":
                    request = self.feedback_service.get_request(int(action["value"]))
                    self.feedback_service.ignore_request(request)
                    self.ignore_request(request, payload["response_url"])
                else:
                    logger.error(f"Unhandled action received: {action['action_id']}")
        else:
            logger.error(f"Unhandled payload received: {payload['type']}")

    def handle_request_feedback(self, payload: dict):
        values = payload["view"]["state"]["values"]
        team_id = payload["user"]["team_id"]
        sender = self.feedback_service.get_user(
            user_id=payload["user"]["id"], team_id=team_id
        )
        self.update_user_profile(sender)
        recipient = self.feedback_service.get_user(
            user_id=values["requestFrom"]["actionFrom"]["selected_user"],
            team_id=team_id,
        )
        self.update_user_profile(recipient)
        request = self.feedback_service.create_request(
            sender, recipient, values["requestMessage"]["actionMessage"]["value"]
        )
        self.ask_feedback(request, recipient.user_id)

    def handle_give_feedback(self, payload: dict):
        values = payload["view"]["state"]["values"]
        team_id = payload["user"]["team_id"]
        author = self.feedback_service.get_user(
            user_id=payload["user"]["id"], team_id=team_id
        )
        self.update_user_profile(author)

        if "giveTo" in values:
            request = None
            recipient = self.feedback_service.get_user(
                user_id=values["giveTo"]["actionTo"]["selected_user"],
                team_id=team_id,
            )
            self.update_user_profile(recipient)
        else:
            callback_id = payload["view"]["callback_id"]
            request = self.feedback_service.get_request(int(callback_id))
            recipient = request.sender
        feedback = self.feedback_service.create_feedback(
            author,
            recipient,
            values["giveStart"]["actionStart"]["value"],
            values["giveContinue"]["actionContinue"]["value"],
            values["giveStop"]["actionStop"]["value"],
            request,
        )
        self.send_feedback(feedback)


class SlackOAuthService:
    AUTHORIZE_URL = "https://slack.com/oauth/v2/authorize"
    ACCESS_TOKEN_URL = "https://slack.com/api/oauth.v2.access"
    SCOPES = (
        "chat:write.public",
        "chat:write",
        "commands",
        "users:read",
        "users:read.email"
    )

    def __init__(self, settings: dict):
        self.settings = settings

    def get_authorization_url(self, redirect_uri: str) -> str:
        query_params = {
            "client_id": self.settings["client_id"],
            "scope": ",".join(self.SCOPES),
            "redirect_uri": redirect_uri,
        }
        url = f"{self.AUTHORIZE_URL}?{urlencode(query_params)}"
        return url

    def get_access_token(self, authorization_code: str) -> dict:
        post_fields = {
            "code": authorization_code,
            "client_id": self.settings["client_id"],
            "client_secret": self.settings["client_secret"],
        }
        response = requests.post(self.ACCESS_TOKEN_URL, data=post_fields)
        return response.json()
