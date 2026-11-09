from django.test import TestCase, Client
from django.contrib.auth import get_user_model

class SyllabusExtractorTests(TestCase):
    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )
        self.client.force_login(self.user)

    def test_invalid_json(self):
        response = self.client.post(
            "/api/extract-syllabus/",
            data="{invalid-json}",
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_syllabus(self):
        response = self.client.post(
            "/api/extract-syllabus/",
            data='{"syllabus": "", "method": "zero_shot"}',
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_large_input(self):
        import json

        response = self.client.post(
            "/api/extract-syllabus/",
            data=json.dumps({
                "syllabus": "A" * 15000,
                "method": "zero_shot"
            }),
            content_type="application/json"
        )
        self.assertIn(response.status_code, [400, 413])