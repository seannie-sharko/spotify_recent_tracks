import creds
import spotipy
import spotipy.util as util
from datetime import datetime
from dateutil import tz
from rich.console import Console
from rich.table import Table

def get_spotify_token():
    """OAuth token for Spotify authentication."""
    token = util.prompt_for_user_token(
        creds.username,
        'user-read-recently-played',
        creds.client_id,
        creds.client_secret,
        creds.redirect_uri
    )
    if not token:
        raise ValueError("Failed to get Spotify token. Please check your credentials.")
    return token

def convert_utc_to_local(utc_time_str):
    """Convert UTC time to local"""
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Parse the UTC time string to a datetime object
    played_at_obj = f"{utc_time_str[:10]} {utc_time_str[11:19]}"  # Format to 'YYYY-MM-DD HH:MM:SS'
    time_obj = datetime.strptime(played_at_obj, '%Y-%m-%d %H:%M:%S').replace(tzinfo=from_zone)

    # Convert to local time and return the formatted string
    return time_obj.astimezone(to_zone).strftime('%Y-%m-%d %H:%M:%S')

def print_recent_tracks(recent_tracks):
    """Print the recent tracks in a rich table"""
    table = Table(show_lines=True, title="Last 35 Spotify Tracks:")
    table.add_column("Artist", justify="left", style="cyan")
    table.add_column("Name", justify="left", style="magenta")
    table.add_column("Album", justify="left", style="green")
    table.add_column("Time", justify="left", style="yellow")
    for item in recent_tracks['items']:
        artist_name = item['track']['artists'][0]['name']
        track_name = item['track']['name']
        album_name = item['track']['album']['name']
        played_at_time = item['played_at']

        # Convert played time from UTC to local time
        local_time = convert_utc_to_local(played_at_time)

        # Add row to the table
        table.add_row(artist_name, track_name, album_name, local_time)

    # Print the table to console
    console = Console()
    console.print(table)

def main():
    """Display recent tracks."""
    try:
        # Get the OAuth token
        token = get_spotify_token()

        # Initialize Spotify client
        spotify = spotipy.Spotify(auth=token)

        # Fetch recent tracks
        recent_tracks = spotify.current_user_recently_played(limit=35)

        # Print the tracks
        print_recent_tracks(recent_tracks)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
