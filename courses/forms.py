from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "course_code",
            "course_name",
            "term",
            "year",
            "office_hours",
            "meeting_schedule",
            "description",
        ]

    def clean_course_code(self):
        return self.cleaned_data["course_code"].strip()

    def clean_course_name(self):
        return self.cleaned_data["course_name"].strip()