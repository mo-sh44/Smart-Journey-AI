import os
import datetime
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

BERLIN_HOLIDAYS = {
    "Neujahrstag", "Internationaler Frauentag", "Karfreitag", "Ostermontag",
    "Tag der Arbeit", "Christi Himmelfahrt", "Pfingstmontag",
    "Tag der Deutschen Einheit", "Erster Weihnachtstag", "Zweiter Weihnachtstag",
}


class CalendarService:
    def __init__(self):
        self.credentials_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "./data/credentials.json")
        self.token_path = "./data/token.json"

    def get_events(self, start_date: str, end_date: str) -> dict:
        creds = self._authenticate()
        try:
            service = build("calendar", "v3", credentials=creds)
            time_min = datetime.datetime.strptime(start_date, "%Y-%m-%d").isoformat() + "Z"
            time_max = datetime.datetime.strptime(end_date, "%Y-%m-%d").isoformat() + "Z"
            result = {"personal": [], "holidays": []}

            personal_items = service.events().list(
                calendarId="primary", timeMin=time_min, timeMax=time_max,
                singleEvents=True, orderBy="startTime"
            ).execute().get("items", [])

            for event in personal_items:
                if event.get("transparency", "opaque") == "opaque":
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    title = event.get("summary", "Untitled")
                    result["personal"].append(
                        {
                            "date": start,
                            "title": title,
                            "availability": self._classify_event(title),
                        }
                    )

            holiday_items = service.events().list(
                calendarId="de.german#holiday@group.v.calendar.google.com",
                timeMin=time_min, timeMax=time_max,
                singleEvents=True, orderBy="startTime"
            ).execute().get("items", [])

            for event in holiday_items:
                title = event.get("summary", "")
                if any(h in title for h in BERLIN_HOLIDAYS):
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    result["holidays"].append({"date": start, "title": title})

            return result
        except HttpError as exc:
            return {"error": str(exc)}

    def _authenticate(self) -> Credentials:
        creds = None
        if os.path.exists(self.token_path):
            creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    if os.path.exists(self.token_path):
                        os.remove(self.token_path)
                    flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.token_path, "w") as f:
                f.write(creds.to_json())
        return creds

    def _classify_event(self, title: str) -> str:
        text = (title or "").lower()
        available_words = ["urlaub", "frei", "ferien", "vacation", "holiday", "available", "reisezeit"]
        if any(word in text for word in available_words):
            return "available"
        return "busy"
