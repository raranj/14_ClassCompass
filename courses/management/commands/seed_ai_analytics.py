
import random
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from courses.models import AIRequestLog


class Command(BaseCommand):
    help = "Create simulated AI analytics data for a demo user."
    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            required=True
        )
        parser.add_argument(
            "--count",
            type=int,
            default=40
        )
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.filter(
            username=options["username"]
        ).first()
        if user is None:
            raise CommandError("User does not exist.")
        count = options["count"]
        if count < 1 or count > 200:
            raise CommandError(
                "Count must be between 1 and 200."
            )
        rng = random.Random(498)
        methods = ["pdf", "docx", "html", "text"]
        now = timezone.now()
        AIRequestLog.objects.filter(
            user=user,
            is_simulated=True
        ).delete()
        for index in range(count):
            method = rng.choice(methods)
            length = rng.randint(500, 12000)
            latency = round(
                5 + length * 0.008
                + rng.uniform(0, 35),
                2
            )
            tokens = int(
                100 + length * 0.04
                + rng.randint(0, 150)
            )
            succeeded = rng.random() > 0.10
            extracted = (
                rng.randint(3, 14)
                if succeeded else 0
            )
            saved = (
                rng.randint(0, extracted)
                if succeeded else 0
            )
            entry = AIRequestLog.objects.create(
                user=user,
                input_method=method,
                syllabus_length=length,
                latency_seconds=latency,
                generated_tokens=(
                    tokens if succeeded else 0
                ),
                extracted_events=extracted,
                saved_events=saved,
                status=(
                    "success"
                    if succeeded else "failure"
                ),
                is_simulated=True,
            )
            days_ago = rng.randint(0, 29)
            AIRequestLog.objects.filter(
                pk=entry.pk
            ).update(
                created_at=now - timedelta(
                    days=days_ago,
                    hours=rng.randint(0, 20)
                )
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Created {count} simulated requests "
                f"for {user.username}."
            )
        )
