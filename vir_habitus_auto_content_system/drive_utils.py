"""Utilities for interacting with Google Drive."""

import io
from pathlib import Path
from typing import List

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

# Scopes required to read files from Drive
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def get_service(creds_path: Path):
    """Authenticate and return the Drive service client."""
    creds = Credentials.from_service_account_file(str(creds_path), scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def list_images_in_folder(service, folder_id: str) -> List[dict]:
    """Return metadata for images stored in the given folder."""
    query = f"'{folder_id}' in parents and mimeType contains 'image/' and trashed = false"
    results = (
        service.files()
        .list(q=query, fields="files(id, name)")
        .execute()
    )
    return results.get("files", [])


def download_file(service, file_id: str, destination: Path) -> None:
    """Download a Drive file to the given destination path."""
    request = service.files().get_media(fileId=file_id)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with io.FileIO(destination, "wb") as fh:
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"Download {int(status.progress() * 100)}%.")
    print("Download complete.")




