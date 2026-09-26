# ClassCompass
ClassCompass is an academic planning application designed to help students organize courses and syllabi in one place.

# Run the Server
python manage.py runserver --settings=ClassCompass.settings.development

## Status

The dashboard route (`/`) is now fully implemented and serves as the
application's home page, displaying an overview of the user's courses
and upcoming academic events.

### Section 1: URL Linking & Navigation

Implemented a full URL → view → template flow: the home page (`/`)
renders the dashboard, a navigation bar in `base.html` links between
Home, Courses, Calendar, and Study Tools using `{% url %}` (no
hardcoded paths), and course list items link to their detail pages
via `get_absolute_url()` implemented on the `Course` model.

Routes implemented and working:
- `/` — Dashboard (home page)
- `/courses/summary/`
- `/courses/`
- `/courses/overview/`
- `/courses/<course_id>/`
- `/calendar/`
- `/study-tools/`