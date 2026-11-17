
import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from courses.models import AIRequestLog, Course


class AIAnalyticsTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username="analytics_test",
            password="test_password_123"
        )
        self.other_user = User.objects.create_user(
            username="other_analytics_test",
            password="test_password_123"
        )
        self.course = Course.objects.create(
            user=self.user,
            course_code="CS 498",
            course_name="Applied AI Systems",
            term="fall",
            year=2026,
        )
        self.client.force_login(self.user)

    @patch("courses.calendar_views.extract_calendar_events")
    def test_extraction_creates_analytics_log(self, mock_extract):
        mock_extract.return_value = {
            "status": "success",
            "model": "Qwen/Qwen3-0.6B",
            "course": "CS 498",
            "count": 2,
            "events": [],
            "latency_seconds": 12.5,
            "generated_tokens": 180,
        }
        response = self.client.post(
            reverse("courses:extract_calendar_events"),
            data=json.dumps({
                "syllabus": "CS 498 syllabus test",
                "method": "zero_shot",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        log = AIRequestLog.objects.get(user=self.user)
        self.assertEqual(log.input_method, "text")
        self.assertEqual(log.syllabus_length, 20)
        self.assertEqual(log.extracted_events, 2)
        self.assertEqual(log.generated_tokens, 180)
        self.assertEqual(log.saved_events, 0)
        self.assertEqual(log.status, "success")
        self.assertEqual(
            response.json()["request_id"],
            log.pk
        )

    def test_calendar_save_updates_analytics(self):
        log = AIRequestLog.objects.create(
            user=self.user,
            input_method="text",
            syllabus_length=250,
            latency_seconds=12.5,
            generated_tokens=180,
            extracted_events=2,
            status="success",
        )
        event = {
            "title": "Homework 1",
            "event_type": "assignment",
            "date": "2026-09-10",
            "time": None,
            "end_time": None,
            "weekday": None,
            "repeats_weekly": False,
            "estimated_hours": 4,
            "description": "",
        }
        response = self.client.post(
            reverse("courses:save_calendar_events"),
            data=json.dumps({
                "course_id": self.course.pk,
                "events": [event],
                "request_id": log.pk,
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["created"], 1)
        log.refresh_from_db()
        self.assertEqual(log.saved_events, 1)

    def test_dashboard_only_shows_current_user(self):
        AIRequestLog.objects.create(
            user=self.other_user,
            input_method="pdf",
            syllabus_length=4000,
            latency_seconds=30,
            generated_tokens=300,
            extracted_events=5,
        )
        response = self.client.get(
            reverse("courses:analytics_dashboard")
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["total_requests"],
            0
        )
