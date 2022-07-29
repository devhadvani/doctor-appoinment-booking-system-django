import datetime
from datetime import timedelta

import pytz

from google.oauth2 import service_account

from googleapiclient.discovery import build

service_account_email = "devhadvani@calander-357714.iam.gserviceaccount.com"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_file('credentials.json')
scoped_credentials = credentials.with_scopes(SCOPES)


def build_service():
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service


def create_event():
    service = build_service()

    start_datetime = datetime.datetime.now(tz=pytz.utc)
    event = (
        service.events()
        .insert(
            calendarId="primary",
            body={
                "summary": "Foo 2",
                "description": "Bar",
                "start": {"dateTime": start_datetime.isoformat()},
                "end": {
                    "dateTime": (start_datetime + timedelta(minutes=15)).isoformat()
                },
            },
        )
        .execute()
    )

    print(event)

create_event()