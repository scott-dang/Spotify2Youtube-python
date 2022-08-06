import spotifyHandler as spotify
import youtubeHandler as youtube
from time import sleep

sp_titles = []
sp_ids = []
yt_ids = []
yt_titles = {}


def clear():
    yt_ids.clear()
    yt_titles.clear()
    sp_titles.clear()
    sp_ids.clear()


def main():

    yt = youtube.authenticateYouTube()

    sp = spotify.authenticateSpotify()

    sp.current_user()

    while (True):
        ans = input(
            'Would you like to convert a playlist from Spotify to Youtube or Youtube to Spotify? [S2Y/Y2S] --> ')
        if (ans.upper() == 'S2Y'):
            clear()
            chosen_playlist = spotify.chooseUserPlaylist(sp)
            playlist_url = chosen_playlist['external_urls']['spotify']
            playlist_name = chosen_playlist['name']

            print('\n==============================\nAccessing the playlist called',
                  end='', flush=True)
            for i in range(3):
                sleep(.3)
                print('.', end='', flush=True)
            print(playlist_name, flush=True)

            ans = input(
                'Would you like to see all the imported tracks? [Y/N] -->').upper()
            while (ans != 'Y' and ans != 'N'):
                print("You chose: " + ans)
                ans = input(
                    'Please input a valid character. [Y/N] -->').upper()
            if (ans == 'Y'):
                spotify.grabTitles(playlist_url, sp_titles, sp, 0, True)
            else:
                spotify.grabTitles(playlist_url, sp_titles,  sp, 0)

            print('==============================\nNumber of tracks detected from Spotify playlist: ' + str(len(sp_titles)))
            print('Now processing Youtube ID\'s, this may take awhile.')
            num_of_tracks = len(sp_titles)
            youtube.grabYoutubeIDS(sp_titles, yt_ids)
            print('Number of Youtube ID\'s processed: ' + str(len(yt_ids)) + "\n==============================\n")
            if (len(yt_ids) == num_of_tracks):
                print("SUCCESS!" + "\n==============================\n")
            else:
                print('ERROR, there was an issue processing the playlist.' + "\n==============================\n")
                return -1

            id_of_playlist = youtube.createYoutubePlaylist(yt)
            youtube.addTrackstoYoutubePlaylist(yt, id_of_playlist, yt_ids)
        elif (ans.upper() == 'Y2S'):
            
            clear()

            playlists = youtube.grabCurrentUsersYoutubePlaylists(yt)
            chosen_playlist = youtube.chooseUserPlaylist(playlists)
            youtube.grabTitlesfromYoutubePlaylist(
                yt, chosen_playlist, yt_titles)

            print('\n==============================')
            print('Now processing Spotify ID\'s, this may take awhile.')

            spotify.grabIDSfromTrackName(sp, yt_titles, sp_ids)
            playlist_id = spotify.createPlaylist(sp)
            spotify.addTitlestoPlaylist(sp, playlist_id, sp_ids)


if __name__ == '__main__':
    main()
