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

class SyllabusExtractionForm(forms.Form):
    syllabus = forms.CharField(
        max_length=5000,
        required=True,
        error_messages={
            'required': 'Syllabus cannot be empty.',
            'max_length': 'Maximum 5000 characters allowed.'
        }
    )
    method = forms.CharField(required=False, initial="zero_shot")

    def clean_method(self):
        method = self.cleaned_data.get("method") or "zero_shot"
        if method not in ("zero_shot", "few_shot"):
            raise forms.ValidationError("Invalid prompting method.")
        return method