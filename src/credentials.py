from google_auth_oauthlib.flow import InstalledAppFlow
from src.logger import logger

def get_credentials():
    """Retrieves Google Calendar API credentials."""
    scopes = ["https://www.googleapis.com/auth/calendar"]

    # Replace with the path to your client secret file
    client_secret_file = "client_secret.json"

    # run local server flow to obtain user authorization via desktop app (localhost)
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes=scopes)
    credentials = flow.run_local_server()
    logger.info("Successfully retrieved Google Calendar API credentials")
    return credentials
