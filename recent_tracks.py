import spotipy
import spotipy.util as util
import creds

token = util.prompt_for_user_token(
        creds.username,
        'user-read-recently-played',
        creds.client_id,
        creds.client_secret,
        creds.redirect_uri
)

"""
Build OAuth token for your Spotify app

Parameters:
    username = 'username'
    scope = 'user-read-recently-played'
    client_id='aaaaaaaaaaaaaaaa1234567890123456'
    client_secret='aaaaaaaaaaaaaaaa1234567890123456'
    redirect_uri='http://127.0.0.1:9999'
"""

spotify = spotipy.Spotify(auth=token)
recent_tracks = spotify.current_user_recently_played(limit=40)

print("Last 40 Tracks:")
print("{:<29} {:<40} {:<0}".format('Artist','Track','Album'))
a = 0
for i in recent_tracks['items']:
    print(str(a + 1) + ".) " + \
    "{:<25} {:<40} {:<0}".format(\
    recent_tracks['items'][a]['track']['artists'][0]['name'], \
    recent_tracks['items'][a]['track']['name'], \
    recent_tracks['items'][a]['track']['album']['name']))
    a += 1
