from flask import Flask, request, jsonify
from flask_apscheduler import APScheduler
import uuid
import json
from datetime import datetime, timedelta
import os
 
app = Flask(__name__)
 
EVENT_FILE = 'events.json'
 
class Config:
    SCHEDULER_API_ENABLED = True
 
app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
 
events = []
 
# Load events from file
def load_events():
    global events
    if os.path.exists(EVENT_FILE):
        with open(EVENT_FILE, 'r') as f:
            events = json.load(f)
 
# Save events to file
def save_events():
    with open(EVENT_FILE, 'w') as f:
        json.dump(events, f, indent=2)
 
# Check for upcoming events
@scheduler.task('interval', id='reminder_task', minutes=1)
def remind_upcoming_events():
    now = datetime.now()
    one_hour = now + timedelta(hours=1)
    for event in events:
        start = datetime.fromisoformat(event['start_time'])
        if now <= start <= one_hour and not event.get('reminded'):
            print(f"Reminder: Upcoming event '{event['title']}' at {event['start_time']}")
            event['reminded'] = True
    save_events()
 
@app.route('/events', methods=['POST'])
def create_event():
    data = request.get_json()
    event = {
        'id': str(uuid.uuid4()),
        'title': data['title'],
        'description': data['description'],
        'start_time': data['start_time'],
        'end_time': data['end_time'],
        'reminded': False
    }
    events.append(event)
    save_events()
    return jsonify({'message': 'Event created successfully!', 'event': event}), 201
 
@app.route('/events', methods=['GET'])
def get_events():
    sorted_events = sorted(events, key=lambda x: x['start_time'])
    return jsonify(sorted_events)
 
@app.route('/events/<event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.get_json()
    for event in events:
        if event['id'] == event_id:
            event.update({k: data[k] for k in data if k in event})
            event['reminded'] = False
            save_events()
            return jsonify({'message': 'Event updated successfully!', 'event': event})
    return jsonify({'error': 'Event not found'}), 404
 
@app.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):
    global events
    events = [e for e in events if e['id'] != event_id]
    save_events()
    return jsonify({'message': 'Event deleted successfully!'})
 
@app.route('/events/search', methods=['GET'])
def search_events():
    query = request.args.get('query', '').lower()
    result = [e for e in events if query in e['title'].lower() or query in e['description'].lower()]
    return jsonify(result)
 
if __name__ == '__main__':
    load_events()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)