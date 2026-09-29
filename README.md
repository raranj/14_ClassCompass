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
via `get_absolute_url()` implemented on the `Course` model. Course
detail pages (`/courses/<int:pk>/`) are rendered by `CourseDetailView`
and display a single course's full information.

Routes implemented and working:
- `/` — Dashboard (home page)
- `/courses/summary/`
- `/courses/`
- `/courses/overview/`
- `/courses/<course_id>/`
- `/calendar/`
- `/study-tools/`

### UI ###
Currently still in progress. 
For the font, chose to use Marcellus SC due to how the capital C looked,
also considering how clean it looked. Font was imported from google fonts(no licensing fee). 
Regarding heading 1, chose a dark color background to make it seem a bit more interesting. The color was chosen 
due to it being similar to black but not quite. Using just black made overall site seem too drab and black and white.
Made the navigations buttons to make it easier to click, due to there being an increased area
as opposed to just a word/sentence with a link attached. Also centered the navigation components within button. Added hover
feature, when cursor hovers over button button changes to a shade of gray. Got rid of the line that
shows for hyperlinks. 
