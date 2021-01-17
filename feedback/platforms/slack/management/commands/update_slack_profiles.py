from django.core.management import BaseCommand

from feedback.models import User
from feedback.platforms import Platform, get_service


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        slack_service = get_service(Platform.SLACK)
        for user in users:
            slack_service.update_user_profile(user)
