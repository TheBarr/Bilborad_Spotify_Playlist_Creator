from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

data_input = input("What year would you like to make playlist of (YYY-MM-DD): ")
url = f"https://www.billboard.com/charts/hot-100/{data_input}/"
response = requests.get(url=url)
html = response.text
soup = BeautifulSoup(html, 'html.parser')

song_titles = soup.select("li #title-of-a-story")
songs = [title.get_text().strip() for title in song_titles]

song_artists =  soup.select(".lrv-u-width-100p .o-chart-results-list__item .c-label")
artists = [author.get_text().strip() for author in song_artists][0::7]

load_dotenv()
ID = os.getenv("ID")
SECRED = os.getenv("SECRED")
URI = os.getenv("URI")
USERNAME = os.getenv("USERNAME")

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id=ID,
    client_secret=SECRED,
    username=USERNAME,
    redirect_uri=URI,
    show_dialog=True,
))

year = data_input.split("-")[0]
user_name = sp.current_user()["id"]
list_of_uris = []

for i in range(len(songs)):
    track_name = songs[i].replace("'", "")
    artist_name = artists[i].split()[0]
    query = f'track:"{track_name}" artist:"{artist_name}"'
    results = sp.search(q=query, type='track', limit=1)
    try:
        uri = results['tracks']['items'][0]['uri']
        list_of_uris.append(uri)
    except IndexError:
        print(f"{songs[i]} doesn't exist in Spotify. Skipped.")
        print(track_name, artist_name)
playlist = sp.user_playlist_create(user=user_name, name=f"Billboard Hot 100 from {data_input}", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=list_of_uris)
