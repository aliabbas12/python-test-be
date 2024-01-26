import os

from django.contrib.auth.management.commands import createsuperuser

from utils.django_overrides import get_user_model


class Command(createsuperuser.Command):
    def handle(self, *args, **options):
        if (
            not options["interactive"]
            and get_user_model()
            .objects.filter(
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL", "dev@menulance.com")
            )
            .exists()
        ):
            return
        return super().handle(*args, **options)
