import os
import copy
from dotenv import load_dotenv
from datetime import date, timedelta
from googleapiclient.discovery import build
from src.credentials import get_credentials
from src.logger import logger

# loading variables from .env file
load_dotenv()

CALENDAR_ID = os.getenv("CALENDAR_ID")

COLOR_MAP = {
    "Dismount": "2",  # Sage, green
    "Standby": "5",  # banana , yellow
    "Mount": "4",  # flamingo /red
}


def insert_event(event_type, date_pointer, credentials):
    """Inserts an all-day event into Google Calendar."""
    service = build("calendar", "v3", credentials=credentials)
    event = {
        "summary": event_type,
        "colorId": COLOR_MAP[event_type],
        "start": {"date": date_pointer.strftime("%Y-%m-%d")},
        "end": {"date": (date_pointer + timedelta(days=2)).strftime("%Y-%m-%d")},
        "allDay": True,
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return


def main():
    credentials = get_credentials()
    start_date = date(2024, 5, 1)
    end_date = date(2025, 12, 31)
    date_pointer = copy.deepcopy(start_date)
    
    event_type = ["Mount", "Dismount", "Standby"]
    event_pointer = 0
    while True:
        if date_pointer > end_date:
            break
        
        logger.info(f"creating event: {date_pointer} {event_type[event_pointer % 3]}")
        insert_event(event_type[event_pointer % 3], date_pointer, credentials)
        event_pointer += 1
        date_pointer = date_pointer + timedelta(days=2)


if __name__ == "__main__":
    main()
