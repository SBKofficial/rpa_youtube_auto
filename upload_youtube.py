# upload_youtube.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from config import CLIENT_SECRETS_FILE, TOKEN_FILE, YOUTUBE_CATEGORY, IS_MADE_FOR_KIDS

SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]


def get_authenticated_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        from google.oauth2.credentials import Credentials
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, video_file, title, description, tags, thumb_path=None, privacy="public"):
    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": YOUTUBE_CATEGORY
        },
        "status": {
            "privacyStatus": privacy,
            "selfDeclaredMadeForKids": IS_MADE_FOR_KIDS
        }
    }

    media = MediaFileUpload(video_file, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload {int(status.progress() * 100)}%")

    print("Uploaded ID:", response["id"])

    if thumb_path:
        try:
            youtube.thumbnails().set(
                videoId=response["id"],
                media_body=MediaFileUpload(thumb_path)
            ).execute()
        except Exception as e:
            print("Thumbnail upload failed:", e)

    return response
