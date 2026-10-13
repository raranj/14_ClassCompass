# ClassCompass: An AI-Powered Study and Workload Planner

**ClassCompass** is a web application designed to help college students organize their courses and manage their academic workload. It brings course information, planning tools, and data summaries together in one place.

**Team 14:** Laasyasri Rangu, Ranjana Rajagopalan, and Haaneol Kang

**Course:** INFO 490 MG, Advanced AI-Web-Apps Development, Fall 2026

## Links

- **Live Website:** https://lrangu2.pythonanywhere.com/
- **GitHub Repository:** https://github.com/raranj/14_ClassCompass

## Features

### Course and Workload Management
- Organize academic course information.
- Manage course-related events and planning information.
- Access the application through its web interface.

### Authentication
- Google OAuth login integration.
- Protected pages and API endpoints for authenticated access.
- A public API endpoint for retrieving aggregate user registration statistics.

### Data Visualization
- Interactive Vega-Lite charts embedded in the website.
- A bar chart displaying monthly user sign-ups.
- Chart data retrieved from the application's internal JSON API.

### Reports and Data Exports
- A reports page with grouped data summaries and totals.
- Downloadable CSV and JSON exports.
- Timestamped export files for organizing downloaded reports.

### API Integration
- Internal Django API endpoints backed by application data.
- JSON responses for retrieving course, event, and registration information.
- External public API integration for retrieving and processing external data.

## Technology Stack

| Component | Technologies |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Django Templates |
| Database | SQLite |
| Authentication | Google OAuth |
| Data Visualization | Vega-Lite |
| HTTP Requests | Python `requests` |
| Deployment | PythonAnywhere |
| Version Control | Git and GitHub |

## Application Structure

The project is organized around a Django application and its supporting configuration, templates, and static files.

```text
14_ClassCompass/
├── ClassCompass/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── courses/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── ...
├── templates/
│   └── courses/
├── data/
│   └── db.sqlite3
├── requirements.txt
├── manage.py
└── README.md
```

*Note: This is a simplified overview. Update the structure if your actual repository uses different filenames or directories.*

## API Endpoints

The application exposes internal endpoints for retrieving application data.

| Endpoint | Purpose | Access |
|---|---|---|
| `/api/public/` | Returns monthly new-user sign-ups and cumulative user totals as JSON | Public |
| `/api/courses/` | Provides course-related data | Verify access configuration |
| `/api/events/` | Provides event-related data | Verify access configuration |

### Example: Public Registration Statistics

**Request**

```http
GET /api/public/
```

**Example response**

```json
{
  "values": [
    {
      "month": "2026-09",
      "new_users": 2,
      "total_users": 2
    },
    {
      "month": "2026-10",
      "new_users": 10,
      "total_users": 12
    }
  ]
}
```

The response is generated from the application's user database. The `new_users` field represents registrations during a month, while `total_users` represents the cumulative registration count.

This endpoint also supplies data to the monthly registration bar chart.

## Running the Project Locally

### Prerequisites

- Python installed
- Git installed
- A Google OAuth configuration if testing Google login locally

### 1. Clone the repository

```bash
git clone https://github.com/raranj/14_ClassCompass.git
cd 14_ClassCompass
```

### 2. Create and activate a virtual environment

On macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Configure the environment variables required by your Django settings and Google OAuth integration. Keep client secrets and other credentials private. Do not commit them to GitHub.

### 5. Apply database migrations

```bash
python manage.py migrate
```

If your project requires additional setup for its initial database or authentication provider, complete that configuration before testing those features.

### 6. Start the development server

Use the development settings configured for your local environment:

```bash
python manage.py runserver
```

Open the local URL printed by Django, typically:

http://127.0.0.1:8000/

## Deployment

ClassCompass is deployed on PythonAnywhere:

https://lrangu2.pythonanywhere.com/

The production deployment uses Django production settings, configured environment variables, and collected static files.

After updating the code on the server, reload the web application through the PythonAnywhere Web tab. If static files change, run the appropriate `collectstatic` command using the project's production settings.

## Future Improvements

Potential improvements include expanding personalized workload planning, improving the integration between course information and scheduling, and adding further data visualizations to support students in understanding their academic workload.

## Contributors

- **Laasyasri Rangu**
- **Ranjana Rajagopalan**
- **Haaneol Kang**

Developed as a team project for INFO 490 MG at the University of Illinois Urbana-Champaign, Fall 2026.
