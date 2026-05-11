import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicData:
    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()
        
        # Authenticate with Spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URL"), 
            scope=os.getenv("SCOPE")
        ))

    def get_portfolio_data(self):
        # Fetch the user's top 5 tracks of all time
        results = self.sp.current_user_top_tracks(limit=5, time_range='long_term')
        portfolio = []

        for track in results['items']:
            track_id = track['id']
            name = track['name']
            artist = track['artists'][0]['name']
            
            # Grab the first image URL if it exists
            album_img = track['album']['images'][0]['url'] if track['album']['images'] else None
            preview_url = track['preview_url']
            popularity = track['popularity']

            # Estimate streams (Popularity is 1-100, this formula generates realistic numbers)
            est_streams = int((popularity ** 3) * 2.5)

            # Apply your 2026 Monetization Floor and standard rates
            gross = 0.0
            if est_streams >= 1000:
                gross = est_streams * 0.004
            
            platform_fee = gross * 0.30
            net = gross - platform_fee

            # We format this dictionary to feed BOTH main.py and database.py perfectly
            track_data = {
                'track_id': track_id,
                'name': name,
                'artist': artist,
                'album_img': album_img,
                'preview_url': preview_url,
                'popularity': popularity,
                'est_streams': est_streams,       
                'total_streams': est_streams,     
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