import os
from dotenv import load_dotenv
from datetime import date, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow


# loading variables from .env file
load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")

COLOR_MAP = {
    "Dismount": "6",  # Green
    "Standby": "10",  # Yellow
    "Mount": "11",  # Red
}


def get_credentials():
    """Retrieves Google Calendar API credentials."""
    scopes = ["https://www.googleapis.com/auth/calendar"]

    # Replace with the path to your client secret file
    client_secret_file = "client_secret.json"

    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes=scopes)
    credentials = flow.run_local_server()
    return credentials


def insert_event(event_type):
    """Inserts an all-day event into Google Calendar."""
    credentials = get_credentials()

    service = build("calendar", "v3", credentials=credentials)

    event = {
        "summary": event_type,
        "colorId": COLOR_MAP[event_type],
        "start": {"date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")},
        "end": {"date": (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")},
        "allDay": True,
    }

    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()


def main():
    """Inserts alternating Dismount, Standby, Mount events until the end of 2024."""
    event_types = ["Dismount", "Standby", "Mount"]
    start_date = date.today()

    for event_type in event_types * ((date(2024, 12, 31) - start_date).days // 4 + 1):
        if date.today() > date(2024, 12, 31):
            break
        insert_event(event_type)


if __name__ == "__main__":
    main()
