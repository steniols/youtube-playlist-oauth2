import os
import pickle
import time
from flask import Flask, jsonify, make_response
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

app = Flask(__name__)


def get_credentials():
    credentials = None

    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets.json',
                scopes=[
                    'https://www.googleapis.com/auth/youtube.readonly'
                ]
            )
            flow.run_local_server(port=8080, prompt='consent',
                                  authorization_prompt_message='')
            credentials = flow.credentials

            with open('token.pickle', 'wb') as f:
                print('Saving Credentials for Future Use...')
                pickle.dump(credentials, f)

    return credentials

@app.route('/videos/<playlist_id>')
def get_videos_list(playlist_id):

    credentials = get_credentials()
    print(credentials)
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.playlistItems().list(
        part="status, contentDetails", playlistId=playlist_id
    )

    items = []

    while request is not None:
        response = request.execute()

        for item in response['items']:
            vid_id = item['contentDetails']['videoId']
            yt_link = f"https://youtu.be/{vid_id}"

            videoRequest = youtube.videos().list(
                part="snippet", id=vid_id
            )
            videoResponse = videoRequest.execute()

            videos = videoResponse['items']

            for video in videos:
                item = {'link': yt_link}
                try:
                    item['titulo'] = video['snippet']['title']
                except KeyError:
                    item['titulo'] = ''

                try:
                    item['tags'] = video['snippet']['tags']
                except KeyError:
                    item['tags'] = []
                try:
                    item['publicacao'] = video['snippet']['publishedAt']
                except KeyError:
                    item['publicacao'] = ''
                try:
                    item['thumbnails'] = video['snippet']['thumbnails']
                except KeyError:
                    item['thumbnails'] = []

                items.append(item)

        request = request = youtube.playlistItems().list_next(request, response)

    return make_response(jsonify(items), 200)
