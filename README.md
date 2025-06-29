# Event Scheduler API (Flask)

A simple Flask-based REST API to manage events — create, view, update, delete, and search. Includes reminders and data persistence using `events.json`.

## Features
- Create events with title, description, start & end time
- View all events (sorted by start time)
- Update or delete existing events
- Search by title/description
- Console reminders for events within 1 hour
- Persistent storage

## How to Run

```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints

| Method | Endpoint               | Description         |
|--------|------------------------|---------------------|
| POST   | /events                | Create event        |
| GET    | /events                | List all events     |
| PUT    | /events/<event_id>     | Update event        |
| DELETE | /events/<event_id>     | Delete event        |
| GET    | /events/search?query=x | Search events       |

## Sample Request (POST /events)
```json
{
  "title": "Doctor Visit",
  "description": "Regular check-up",
  "start_time": "2025-06-29T15:30:00",
  "end_time": "2025-06-29T16:00:00"
}
```

## Files
- app.py – Main Flask code
- events.json – Event storage (initial content: [])
- requirements.txt – Dependencies
- postman_collection.json – Ready for Postman import

## Deployment (Optional)
Use Render (https://render.com), Replit (https://replit.com), or PythonAnywhere (https://pythonanywhere.com) for free hosting.

Contact: Ankit Agarwal – +91-8800254925
