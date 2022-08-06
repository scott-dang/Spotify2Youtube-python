import os
import googleapiclient, googleapiclient.discovery
import google_auth_oauthlib
import time
import concurrent.futures
import requests
from googleapiclient.errors import HttpError as httperror

def authenticateYouTube():

    youtube_api_key = os.getenv('youtube_api_key')
    youtube_client_id = os.getenv('youtube_client_id')
    youtube_client_secret = os.getenv('youtube_client_secret')

    api_service_name = 'youtube'
    api_version = 'v3'
    DEVELOPER_KEY = youtube_api_key

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', ['https://www.googleapis.com/auth/youtubepartner'])
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    return youtube


def grabYoutubeURL(track):

    youtube_scraper_REQUEST = 'https://youtube-scrape-sd.herokuapp.com/api/search?q=' + track
    return (requests.get(youtube_scraper_REQUEST).json()['results'][0]['video']['id'])


def grabYoutubeIDS(tracks, video_ids):
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(grabYoutubeURL, tracks)

    for result in results:
        video_ids.append(result)
    print(video_ids)


def createYoutubePlaylist(youtubeObj):

    playlist_title = input('What do you wish to name your playlist? --> ')
    playlist_description = input('Please type up a description. --> ')

    request = youtubeObj.playlists().insert(
        part='snippet,status',
        body={
            'snippet': {
                'title': playlist_title,
                'description': playlist_description,
                'defaultLanguage': 'en'
            },
            'status': {
                'privacyStatus': 'private'
            }
        }
    )
    response = request.execute()

    print(response['id'])
    return response['id']


def addTrackstoYoutubePlaylist(youtubeObj, playlistId, video_ids):

    num_of_ids = len(video_ids)
    for i in range(num_of_ids):
        print('YT ID: ' + str(video_ids[-1]))

        request = youtubeObj.playlistItems().insert(
            part='snippet',
            body={
                'snippet':
                {
                    'playlistId': playlistId,
                    'position': i,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_ids[-1]
                    }
                }
            }
        )

        ctr = 0
        while (True):
            try:
                print('ID: ' + video_ids[-1])
                ctr += 1
                response = request.execute()
                video_ids.pop()
                break
            except httperror as err:
                print('==============EXCEPTION==============')
                print('===========RETRY ATTEMPT ' + (ctr+1) + '/5' + '===========')
                if (ctr == 5):
                    break
                time.sleep(1 / (.5**ctr))


def grabTitlesfromYoutubePlaylist(youtubeObj, playlistId, youtube_video_titles):

    request = youtubeObj.playlistItems().list(
        part='snippet',
        maxResults=50,
        playlistId=playlistId,
    )
    response = request.execute()

    for video in response['items']:
        artist = ''
        if video['snippet']['title'].upper() != 'PRIVATE VIDEO':
            if (video['snippet']['title'].find('ft') == -1):
                artist = video['snippet']['videoOwnerChannelTitle']
            youtube_video_titles[video['snippet']['title']] = artist
    try:
        nextPageToken = response['nextPageToken']
        while (nextPageToken):
            request = youtubeObj.playlistItems().list(
                part='snippet,contentDetails,status,id',
                maxResults=50,
                playlistId=playlistId,
                pageToken=nextPageToken
            )
            response = request.execute()

            for video in response['items']:
                artist = ''

                if video['snippet']['title'].upper() != 'PRIVATE VIDEO':
                    if (video['snippet']['title'].find('ft') == -1):
                        artist = video['snippet']['videoOwnerChannelTitle']
                    youtube_video_titles[video['snippet']['title']] = artist
            nextPageToken = response['nextPageToken']

    except KeyError:
        print('No more pages.')

    return youtube_video_titles

def grabCurrentUsersYoutubePlaylists(youtubeObj):

    youtube_playlists = []
    request = youtubeObj.playlists().list(
        part="snippet,contentDetails",
        maxResults=50,
        mine=True
    )

    response = request.execute()

    for playlist in response['items']:
        youtube_playlists.append(playlist)

    try:
        nextPageToken = response['nextPageToken']
        while (nextPageToken):
            request = youtubeObj.playlists().list(
                part="snippet,contentDetails",
                maxResults=50,
                mine=True,
                pageToken=nextPageToken
            )
            response = request.execute()

            for playlist in response['items']:
                youtube_playlists.append(playlist)
            nextPageToken = response['nextPageToken']

    except KeyError:
        print('No more pages.')
    return youtube_playlists

def chooseUserPlaylist(playlists):
    ctr = 1
    print('\n==============================')
    print('Detected ' + str(len(playlists)) + ' playlists.')
    for title in playlists:
        print('Playlist ' + str(ctr) + ': ' + title['snippet']['title'])
        ctr += 1

    max = len(playlists)
    if (max == 0):
        raise ValueError('Playlist has to have 1 or more tracks')

    print('==============================')
    ans = int(
        input('Which playlist do you want to convert? [1 - ' + str(max) + '] --> '))
    while (ans < 1 or ans > max):
        ans = int(
            input('Please input a valid playlist value. [1 - ' + str(max) + '] --> '))
    return playlists[ans-1]['id']