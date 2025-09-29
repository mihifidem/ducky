from django.core.management.base import BaseCommand
from account.cv_manager.factories import UserFactory, CVFactory

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for _ in range(10):
            user = UserFactory()
            CVFactory.create_batch(2, user=user)