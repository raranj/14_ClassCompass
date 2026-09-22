# ClassCompass
ClassCompass is an academic planning application designed to help students organize courses and syllabi in one place.

# Run the Server
python manage.py runserver --settings=ClassCompass.settings.development

## Status
The main dashboard route (`/`) has been planned in the application
structure, but its final dashboard template has not yet been implemented.
So for now, the dashboard is incomplete and says template not found.

For Assignment 2, the required Django view and template functionality
is implemented and working through these routes:

- `/courses/summary/`
- `/courses/`
- `/courses/overview/`
- `/courses/<course_id>/`