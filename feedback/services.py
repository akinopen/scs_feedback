from typing import Optional, Sequence

from feedback.models import Feedback, Request, User

__all__ = ("FeedbackService",)


class FeedbackService:
    @staticmethod
    def get_user(user_id: str, team_id: str) -> User:
        return User.objects.get_or_create(user_id=user_id, team_id=team_id)[0]

    @staticmethod
    def get_request(request_id: int):
        return Request.objects.get(id=request_id)

    @staticmethod
    def create_request(
        sender: User, recipients: Sequence[User], message: Optional[str]
    ) -> Request:
        request = Request.objects.create(sender=sender, message=message)
        request.recipients.add(*recipients)
        return request

    @staticmethod
    def create_feedback(
        author: User,
        recipient: User,
        start_doing: str,
        continue_doing: str,
        stop_doing: str,
        feedback_request: Optional[Request] = None,
    ):
        feedback = Feedback.objects.create(
            author=author,
            recipient=recipient,
            start_doing=start_doing,
            continue_doing=continue_doing,
            stop_doing=stop_doing,
            request=feedback_request,
        )
        if feedback_request:
            feedback_request.status = Request.Status.REPLIED.value
            feedback_request.save()
        return feedback

    @staticmethod
    def ignore_request(feedback_request: Request):
        feedback_request.status = Request.Status.IGNORED.value
        feedback_request.save()
