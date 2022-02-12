"""
This is a simple table builder to display your last 40 tracks
you've listened to in Spotify using Spotipy.
---Spotipy: https://github.com/plamere/spotipy
"""

import creds
import spotipy
import spotipy.util as util
from datetime import datetime
from dateutil import tz

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
# Build table headers
print("{:<29} {:<50} {:<40} {:<0}".format('Artist','Name','Album', 'Time'))
a = 0
for i in recent_tracks['items']:

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Spotify returns 'played_at' time in non-standard format
    # parse out non-standard chars
    played_at_time = recent_tracks['items'][a]['played_at'] # 2000-01-01T00:00:00.000Z
    played_at_obj = str(played_at_time[0:10]) \
    + " " + \
    str(played_at_time[11:19]) # 2000-01-01 00:00:00 --BUT UTC!!

    # Convert str to datetime obj in order to change tz | (2000-01-01 00:00:00+00:00)
    time_obj = datetime.strptime(played_at_obj, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)

    # Convert datetime obj from UTC tz to user's local tz | (2000-01-01 00:00:00)
    local_time = time_obj.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')

    # Build table underneath headers
    print(str(a + 1) + ".) " + \
    "{:<25} {:<50} {:<40} {:<0}".format(\
    recent_tracks['items'][a]['track']['artists'][0]['name'], \
    recent_tracks['items'][a]['track']['name'], \
    recent_tracks['items'][a]['track']['album']['name'], \
    local_time))

    a += 1
