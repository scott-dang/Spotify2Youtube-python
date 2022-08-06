import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

def authenticateSpotify():
    load_dotenv()
    spotify_client_id = os.getenv('spotify_client_id')
    spotify_client_secret = os.getenv('spotify_client_secret')
    spotifyObj = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                    client_secret=spotify_client_secret,
                                                    redirect_uri='http://127.0.0.1:5500',
                                                    scope=['playlist-read-private', 'playlist-modify-public']))
    return spotifyObj

def chooseUserPlaylist(spotifyObj=None):
    output = '=============================='
    playlists = spotifyObj.current_user_playlists()['items']
    for i in range(len(playlists)):
        output += '\n' + str(i+1) + ' : ' + playlists[i]['name']
    max = len(playlists)
    if (max == 0):
        raise ValueError('Playlist has to have 1 or more tracks')

    print(output)
    ans = int(
        input('Which playlist do you want to convert? [1 - ' + str(max) + '] --> '))
    while (ans < 1 or ans > max):
        ans = int(
            input('Please input a valid playlist value. [1 - ' + str(max) + '] --> '))
    return playlists[ans-1]


def grabTitles(url, tracks, spotifyObj, offset=0, printOut=False):
    index = url.find('/playlist/') + 10
    playlist_id = (url.split('?si=', 1)[0])
    playlist_id = playlist_id[index:]
    playlist = spotifyObj.playlist_tracks(playlist_id, 'items', 100, offset)

    for item in playlist['items']:
        tracks.append(item['track']['name'] + ' by ' +
                      item['track']['album']['artists'][0]['name'])
        if (printOut):
            print(tracks[-1])
    while (len(tracks) != spotifyObj.playlist_tracks(url)['total']):
        grabTitles(url, tracks, spotifyObj, offset + 100)
    return spotifyObj.playlist(url)['name']


def grabIDSfromTrackName(spotifyObj, trackNames, spotifyTrackIds):
    invalid_songs = []
    valid_songs = []

    for name in trackNames.keys():
        print('BEFORE SEARCH QUERY: ' + name + ' ' + artist)
        artist = trackNames[name].replace('VEVO', '').replace('vevo', '')
        filtered_name = name.upper().replace('OFFICIAL', '').replace(
            'AUDIO', '').replace('VISUALIZER', '').replace('MUSIC', '').replace('VIDEO', '')
        filtered_name = filtered_name.replace('(', '').replace(')', '')
        print('ARTIST: ' + artist)
        if (artist != '' and filtered_name.find(artist.upper()) != -1):
            artist = ''
        print('AFTER SEARCH QUERY: ' + filtered_name + ' ' + artist + '\n')
        response = spotifyObj.search(
            filtered_name + ' ' + artist, 10, 0, 'track')

        if not response['tracks']['items']:
            invalid_songs.append(name)
        else:
            valid_songs.append(name)
            spotifyTrackIds.append(response['tracks']['items'][0]['id'])
    print('==============================')
    print(str(len(invalid_songs)) +
          ' songs have not been successfully processed due to no result on Spotify.')
    print('MISSING SONGS: ' + str(invalid_songs))
    print(str(len(spotifyTrackIds)) + ' songs have been processed.\n')
    print('ADDED SONGS: ' + str(valid_songs) +
          '\n==============================')
    return spotifyTrackIds


def createPlaylist(spotifyObj):
    user_id = spotifyObj.current_user()['id']
    name = input('What do you wish to name your playlist? --> ')
    description = input('Please type up a description. --> ')
    return spotifyObj.user_playlist_create(user_id, name, True, False, description)['id']


def addTitlestoPlaylist(spotifyObj, playlistId, spotifyTrackIds):
    init_size = len(spotifyTrackIds)
    spotifyTrackIds = list(dict.fromkeys(spotifyTrackIds))
    final_size = len(spotifyTrackIds)
    print('\n==============================\n' +
          str(init_size - final_size) + ' duplicates have been removed.')

    while (len(spotifyTrackIds) > 100):
        spotifyObj.playlist_add_items(playlistId, spotifyTrackIds[0:100])
        for i in range(100):
            spotifyTrackIds.pop(0)
    spotifyObj.playlist_add_items(playlistId, spotifyTrackIds)
