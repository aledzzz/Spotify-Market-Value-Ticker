import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

class MusicData:
    def __init__(self):
        load_dotenv()
        
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=os.getenv("CLIENT_ID"),
            client_secret=os.getenv("CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URL"), 
            scope=os.getenv("SCOPE")
        ))

    def get_portfolio_data(self):
        results = self.sp.current_user_top_tracks(limit=5, time_range='long_term')
        portfolio = []

        for track in results['items']:
            track_id = track['id']
            name = track['name']
            artist = track['artists'][0]['name']
            
            album_img = track['album']['images'][0]['url'] if track['album']['images'] else None
            preview_url = track.get('preview_url')
            est_streams = random.randint(50, 2500000)

            gross = 0.0 
            if est_streams >= 1000:
                gross = est_streams * 0.004
            
            platform_fee = gross * 0.30
            net = gross - platform_fee

            track_data = {
                'track_id': track_id,
                'name': name,
                'artist': artist,
                'album_img': album_img,
                'preview_url': preview_url,
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