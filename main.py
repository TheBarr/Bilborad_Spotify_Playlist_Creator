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

load_dotenv()
ID = os.getenv("ID")
SECRED = os.getenv("SECRED")
URI = os.getenv("URI")

scope = "playlist-modify-private"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope=scope,
    client_id=ID,
    client_secret=SECRED,
    username="DraV",
    redirect_uri=URI,
    show_dialog= True,
))

results = sp.current_user_saved_tracks()
