from django.contrib import admin
from .models import Course, Syllabus, AcademicEvent, GradeItem, StudyTool

admin.site.register(Course)
admin.site.register(Syllabus)
admin.site.register(AcademicEvent)
admin.site.register(GradeItem)
admin.site.register(StudyTool)