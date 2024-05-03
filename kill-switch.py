from googleapiclient.discovery import build
import os
from dotenv import load_dotenv
from src.credentials import get_credentials

# Replace with your credentials file path
CREDENTIALS_FILE = "credentials.json"

# Define the calendar ID (primary by default)
load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")

# Define scopes for authorization
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def delete_events():
    """Deletes all events from the specified calendar."""
    credentials = get_credentials()
    service = build("calendar", "v3", credentials=credentials)

    # Retrieve upcoming events (can be adjusted for specific time range)
    events = service.events().list(calendarId=CALENDAR_ID).execute().get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    for event in events:
        event_id = event["id"]
        service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(f'Event deleted: {event.get("summary", "Unnamed Event")}')


if __name__ == "__main__":
    delete_events()
    print("All events deleted (if any).")
