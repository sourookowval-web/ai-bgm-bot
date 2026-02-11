import os
from google.oauth2.credentials import Credentials
import googleapiclient.discovery

def upload(title):
    creds = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"]
    )

    youtube = googleapiclient.discovery.build("youtube","v3",credentials=creds)

    youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet":{"title":title,"description":"AI Generated BGM"},
            "status":{"privacyStatus":"public"}
        },
        media_body="out.mp4"
    ).execute()
