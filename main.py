from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

inp = input("Which year do you want to travel to?  Type the date in this format YYYY-MM-DD:\n")

response = requests.get("https://www.billboard.com/charts/hot-100/" + inp)
response.raise_for_status()
webpage = response.text
soup = BeautifulSoup(webpage, "html.parser")

top_100_info = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
top_100_names = [i.text for i in top_100_info]

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri=os.environ.get("SPOTIPY_REDIRECT_URI"),
    client_id=os.environ.get("SPOTIPY_CLIENT_ID"),
    client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET"),
    show_dialog=True,
    cache_path="token.txt"

))

top_100_urls = []
for i in top_100_names:
    item = sp.search(q=f"track:{i} year:{inp[:4]}", limit=1)
    try:
        top_100_urls.append(item['tracks']['items'][-1]['external_urls']['spotify'])
    except IndexError:
        pass

user_id = sp.current_user()['id']

playlist = sp.user_playlist_create(user=user_id, name=f"Top 100 songs of {inp}",
                                   public=False)
sp.playlist_add_items(playlist_id=playlist['id'], items=top_100_urls)
