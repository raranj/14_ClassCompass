import unittest
from unittest.mock import MagicMock, patch

from courses.calendar_ai import (
    split_syllabus,
    parse_event_json,
    validate_event,
    extract_calendar_events,
)


class CalendarAITests(unittest.TestCase):

    def test_split_syllabus(self):
        text = "Assignment 1\n" * 100

        sections = split_syllabus(
            text,
            max_chars=200
        )

        self.assertGreater(len(sections), 1)

    def test_parse_multiple_events(self):
        output = """
        {
            "course": "ECE 391",
            "events": [
                {
                    "title": "MP1",
                    "event_type": "assignment",
                    "date": "2026-09-10"
                },
                {
                    "title": "MP2",
                    "event_type": "assignment",
                    "date": "2026-09-24"
                },
                {
                    "title": "Midterm",
                    "event_type": "exam",
                    "date": "2026-10-15"
                }
            ]
        }
        """

        result = parse_event_json(output)

        self.assertEqual(len(result["events"]), 3)
        self.assertEqual(
            result["events"][2]["event_type"],
            "exam"
        )

    def test_invalid_json(self):
        with self.assertRaises(ValueError):
            parse_event_json("This is not JSON")

    def test_missing_date(self):
        event = {
            "title": "Homework 1",
            "event_type": "assignment",
            "date": None,
            "time": None,
            "end_time": None,
            "weekday": None,
            "repeats_weekly": False,
            "estimated_hours": None,
            "description": None
        }

        result = validate_event(event)

        self.assertIsNone(result["date"])

    def test_weekly_office_hours(self):
        event = {
            "title": "Professor Office Hours",
            "event_type": "office_hours",
            "date": None,
            "time": "14:00",
            "end_time": "16:00",
            "weekday": "monday",
            "repeats_weekly": True,
            "estimated_hours": None,
            "description": None
        }

        result = validate_event(event)

        self.assertTrue(result["repeats_weekly"])
        self.assertEqual(result["weekday"], "monday")
        self.assertEqual(result["time"], "14:00")

    def test_invalid_weekday(self):
        event = {
            "title": "Office Hours",
            "event_type": "office_hours",
            "date": None,
            "time": "14:00",
            "weekday": "notaday",
            "repeats_weekly": True
        }

        with self.assertRaises(ValueError):
            validate_event(event)


    @patch("courses.calendar_ai.get_model_and_tokenizer")
    def test_extract_seven_calendar_events(self, mock_loader):
        """
        Verify that the extraction pipeline handles
        assignments, exams, quizzes, and recurring office hours.
        No model download is needed for this test.
        """
        from courses.calendar_ai import extract_calendar_events

        syllabus = """
ECE 391 - Computer Systems Engineering
Fall 2026

MP1: System Calls - Due September 10, 2026 - Estimated 8 hours
MP2: File Systems - Due September 24, 2026 - Estimated 12 hours
MP3: Processes and Threads - Due October 15, 2026 - Estimated 15 hours

Midterm Exam: October 22, 2026 at 7:00 PM
Quiz 1: September 17, 2026 at 2:00 PM
Office Hours: Every Monday and Wednesday from 2:00 PM to 4:00 PM
"""

        # Reproduce the six events Qwen generated during our test.
        # The pipeline should expand office hours to seven.
        model_response = """
{
  "course": "ECE 391",
  "events": [
    {"title": "MP1: System Calls",
     "event_type": "assignment", "date": "2026-09-10",
     "time": null, "end_time": null, "weekday": null,
     "repeats_weekly": false, "estimated_hours": 8,
     "description": null},
    {"title": "MP2: File Systems",
     "event_type": "assignment", "date": "2026-09-24",
     "time": null, "end_time": null, "weekday": null,
     "repeats_weekly": false, "estimated_hours": 12,
     "description": null},
    {"title": "MP3: Processes and Threads",
     "event_type": "assignment", "date": "2026-10-15",
     "time": null, "end_time": null, "weekday": null,
     "repeats_weekly": false, "estimated_hours": 15,
     "description": null},
    {"title": "Midterm Exam",
     "event_type": "exam", "date": "2026-10-22",
     "time": "2026-09-10T17:00:00Z",
     "end_time": "2026-10-22T19:00:00Z",
     "weekday": "Monday", "repeats_weekly": false,
     "estimated_hours": null, "description": null},
    {"title": "Quiz 1",
     "event_type": "quiz", "date": "2026-09-17",
     "time": "2026-09-10T15:00:00Z",
     "end_time": "2026-09-10T17:00:00Z",
     "weekday": "Monday", "repeats_weekly": false,
     "estimated_hours": null, "description": null},
    {"title": "Office Hours",
     "event_type": "office_hours", "date": "2026-09-10",
     "time": "2026-09-10T14:00:00Z",
     "end_time": "2026-09-10T16:00:00Z",
     "weekday": "Monday", "repeats_weekly": true,
     "estimated_hours": null, "description": null}
  ]
}
"""

        tokenizer = MagicMock()
        model = MagicMock()

        # The implementation slices model output after the prompt.
        import torch
        tokenizer.apply_chat_template.return_value = {
            "input_ids": torch.tensor([[1]]),
            "attention_mask": torch.tensor([[1]]),
        }
        tokenizer.eos_token_id = 0
        tokenizer.decode.return_value = model_response

        # One prompt token + one generated token.
        model.generate.return_value = torch.tensor([[1, 2]])
        mock_loader.return_value = (tokenizer, model)

        result = extract_calendar_events(syllabus)

        self.assertEqual(result["count"], 7)

        events = result["events"]
        by_title = {e["title"]: e for e in events
                    if e["event_type"] != "office_hours"}

        self.assertEqual(by_title["MP1: System Calls"]["date"], "2026-09-10")
        self.assertEqual(by_title["MP1: System Calls"]["estimated_hours"], 8)
        self.assertEqual(by_title["Midterm Exam"]["event_type"], "exam")
        self.assertEqual(by_title["Midterm Exam"]["time"], "19:00")
        self.assertEqual(by_title["Quiz 1"]["time"], "14:00")

        office_hours = [
            e for e in events if e["event_type"] == "office_hours"
        ]
        self.assertEqual(len(office_hours), 2)
        self.assertEqual(
            {e["weekday"] for e in office_hours},
            {"monday", "wednesday"}
        )
        self.assertTrue(all(e["repeats_weekly"] for e in office_hours))
        self.assertTrue(all(e["time"] == "14:00" for e in office_hours))
        self.assertTrue(all(e["end_time"] == "16:00" for e in office_hours))
