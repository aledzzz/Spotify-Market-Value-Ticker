import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicData:
    def __init__(self):
        load_dotenv()
        
        self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(client_id = os.getenv("CLIENT_ID"), client_secret = os.getenv("CLIENT_SECRET"), redirect_uri = os.getenv("REDIRECT_URL"), scope = os.getenv("SCOPE")))

    def get_portfolio_data(self):
        current_streams = {
            "delusional": 37855457,
            "Habits": 15921294,
            "I Rot, I Rot.": 8401491,
            "I Thought She Knew": 7922684,
            "Studio Addict": 3911171
        }

        results = self.sp.current_user_top_tracks(limit = 5, time_range = "long_term")
        portfolio = []

        for track in results["items"]:
            track_id = track["id"]
            name = track["name"]
            artist = track["artists"][0]["name"]

            album_img = track["album"]["images"][0]["url"] if track["album"]["images"] else None
            preview_url = track.get("preview_url")
            
            true_streams = current_streams.get(name)
            if true_streams is None:
                print(f"Spotify streams for {name} by {artist} is not available")
                user_input = input("Enter current Spotify streams for this track (or press Enter to simulate streams): ")

                if user_input.isdigit():
                    true_streams = int(user_input)
                else:
                    print("Simulating streams...")
                    true_streams = random.randint(500000, 2500000)

            gross = 0.0
            if true_streams >= 1000:
                gross = true_streams * 0.004
            
            platform_fee = gross * 0.30
            net = gross - platform_fee

            track_data = {
                'track_id': track_id,
                'name': name,
                'artist': artist,
                'album_img': album_img,
                'preview_url': preview_url,
                'est_streams': true_streams,       
                'total_streams': true_streams,     
                'gross': gross,                    
                'platform_fee': platform_fee,      
                'net_royalty_pool': net,           
                'finances': {                      
                    'gross': gross,
                    'fee': platform_fee,
                    'net': net
                }
            }
            portfolio.append(track_data)
            
        return portfolio