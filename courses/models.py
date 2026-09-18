from django.db import models
from django.conf import settings

class Course(models.Model):
    """
    Represents a course that a student is taking.

    A course stores basic course information and connects the student's
    syllabus, academic events, grades, and study tools.
    """

    TERM_CHOICES = [
        ("spring", "Spring"),
        ("summer", "Summer"),
        ("fall", "Fall"),
        ("winter", "Winter"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
    course_name = models.CharField(max_length=150)
    term = models.CharField(max_length=10, choices=TERM_CHOICES)
    year = models.PositiveSmallIntegerField()
    office_hours = models.TextField(blank=True)
    meeting_schedule = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["course_code"]

        constraints = [
            models.UniqueConstraint(fields=["user", "course_code", "term", "year"], name="unique_course_per_user_term")
        ]

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"



class Syllabus(models.Model):
    """
    Represents a syllabus uploaded by a student for one of their courses.

    This model exists because syllabus upload and AI extraction are core features.
    The uploaded syllabus provides the material used to extract course information
    and academic events.
    """

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("complete", "Complete"),
        ("failed", "Failed"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    file = models.FileField(upload_to="syllabi/")
    version = models.PositiveIntegerField(default=1)
    is_current = models.BooleanField(default=True)
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    processing_error = models.TextField(blank=True)

    class Meta:
        ordering = ["-version"]

        constraints = [
            models.UniqueConstraint(fields=["course", "version"], name="unique_syllabus_version_per_course")
        ]

    def __str__(self):
        return (
            f"{self.course.course_code} Syllabus "
            f"(Version {self.version})"
        )



class AcademicEvent(models.Model):
    """
    Represents an academic deadline, assessment, or other scheduled course activity.

    This model exists because ClassCompass converts syllabus information
    into editable events that populate the calendar.
    """

    EVENT_TYPE_CHOICES = [
        ("assignment", "Assignment"),
        ("quiz", "Quiz"),
        ("exam", "Exam"),
        ("project", "Project"),
        ("reading", "Reading"),
        ("presentation", "Presentation"),
        ("discussion", "Discussion"),
        ("lab", "Lab"),
        ("other", "Other"),
    ]

    SOURCE_CHOICES = [
        ("ai", "AI Extracted"),
        ("manual", "Manually Added"),
    ]

    ESTIMATE_SOURCE_CHOICES = [
        ("ai", "AI Estimated"),
        ("manual", "User Entered"),
        ("unknown", "Unknown"),
    ]

    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default="other")
    description = models.TextField(blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    all_day = models.BooleanField(default=False)
    estimated_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    estimate_source = models.CharField(max_length=10, choices=ESTIMATE_SOURCE_CHOICES, default="unknown")
    source = models.CharField(max_length=10, choices=SOURCE_CHOICES, default="manual")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")

    class Meta:
        ordering = ["scheduled_at", "title"]

        constraints = [
            models.UniqueConstraint(fields=["course", "title", "event_type"], name="unique_event_per_course")
        ]

    def __str__(self):
        return f"{self.course.course_code}: {self.title}"



class GradeItem(models.Model):
    """
    Represents an individual graded component within a student's course.

    This model exists to support the basic course-specific Grades section
    in the app. It allows students to record graded assignments,
    exams, projects, participation, and other grades.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    points_earned = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    points_possible = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    weight_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    is_extra_credit = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["category", "name"]

        constraints = [
            models.UniqueConstraint(fields=["course", "name", "category"], name="unique_grade_item_per_course")
        ]

    def __str__(self):
        return f"{self.course.course_code}: {self.name}"



class StudyTool(models.Model):
    """
    Represents an AI-generated study resource for a specific course.

    This model exists so students can select academic events or provide
    additional course material and ask ClassCompass to generate resources
    such as study guides, summaries, or practice questions.
    """

    TOOL_TYPE_CHOICES = [
        ("study_guide", "Study Guide"),
        ("practice_questions", "Practice Questions"),
        ("summary", "Summary"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("generating", "Generating"),
        ("complete", "Complete"),
        ("failed", "Failed"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    related_events = models.ManyToManyField(AcademicEvent, blank=True)
    title = models.CharField(max_length=200)
    tool_type = models.CharField(max_length=30, choices=TOOL_TYPE_CHOICES)
    source_text = models.TextField(blank=True)
    source_file = models.FileField(upload_to="study_materials/", null=True, blank=True)
    custom_instructions = models.TextField(blank=True)
    generated_content = models.TextField(blank=True)
    generation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        ordering = ["title"]

        constraints = [
            models.UniqueConstraint(fields=["course", "title", "tool_type"], name="unique_study_tool_per_course")
        ]

    def __str__(self):
        return f"{self.course.course_code}: {self.title}"