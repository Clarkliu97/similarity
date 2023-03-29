from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import io
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


# Set up the OAuth2 authentication flow
flow = InstalledAppFlow.from_client_secrets_file(
    'client_secret.json',
    scopes=['https://www.googleapis.com/auth/drive']
)
creds = flow.run_local_server(port=9005)
drive_service = build('drive', 'v3', credentials=creds)

results = drive_service.files().list(
    fields="files(name,id,createdTime, modifiedTime, owners, lastModifyingUser)"
).execute()

items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(item)
        print('---------------------')


# Download a file from Google Drive
file_id = '1kyW07iHNJ1fmzYFhp_KxFFeajdu_M2g5'
request = drive_service.files().get_media(fileId=file_id)
file = io.BytesIO()
downloader = MediaIoBaseDownload(file, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print("Download %d%%." % int(status.progress() * 100))

# Save the downloaded file to disk
with open('example1.doc', 'wb') as f:
    f.write(file.getbuffer())

# Upload a file to Google Drive
file_name = 'example.txt'
file_metadata = {'name': file_name}
media = MediaFileUpload(file_name, resumable=True)
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
print(f'File ID: {file.get("id")}')
