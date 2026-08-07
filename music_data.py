import os
import random
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
import sqlite3

class MusicData:
    def __init__(self):
        load_dotenv()
        self.offline_fallback = False
        try:
            self.sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
                client_id = os.getenv("CLIENT_ID"), 
                client_secret = os.getenv("CLIENT_SECRET"), 
                redirect_uri = os.getenv("REDIRECT_URL"), 
                scope = os.getenv("SCOPE")
            ))
        except Exception:
            self.offline_fallback = True

    def get_portfolio_data(self):
        portfolio = []
        current_streams = {
            "delusional": 37855457,
            "Habits": 15921294,
            "I Rot, I Rot.": 8401491,
            "I Thought She Knew": 7922684,
            "Studio Addict": 3911171
        }

        if not self.offline_fallback:
            try:
                results = self.sp.current_user_top_tracks(limit = 5, time_range = "long_term")
                for track in results["items"]:
                    track_id = track["id"]
                    name = track["name"]
                    artist = track["artists"][0]["name"]
                    album_img = track["album"]["images"][0]["url"] if track["album"]["images"] else None
                    
                    true_streams = current_streams.get(name, 1000000)
                    gross = true_streams * 0.004
                    platform_fee = gross * 0.30
                    net = gross - platform_fee

                    portfolio.append({
                        'track_id': track_id,
                        'name': name,
                        'artist': artist,
                        'album_img': album_img,
                        'est_streams': true_streams,       
                        'total_streams': true_streams,     
                        'gross': gross,                    
                        'platform_fee': platform_fee,      
                        'net_royalty_pool': net,           
                        'finances': {'gross': gross, 'fee': platform_fee, 'net': net}
                    })
                return portfolio
            except (SpotifyException, Exception) as e:
                print(f"\nSpotify API unavailable [i stopped paying for spotify premium, sorry :( ]")
        
        # Fallback to database if premium is unavailable
        return self._get_data_from_db()

    def _get_data_from_db(self):
        portfolio = []
        
        # Hardcoded dictionary due to my loss of Spotify Premium :(
        current_streams = {
            "delusional": 37855457,
            "Habits": 15921294,
            "I Rot, I Rot.": 8401491,
            "I Thought She Knew": 7922684,
            "Studio Addict": 3911171
        }
        
        # Failsafe for visuals incase the database is missing or empty
        mock_ui_data = [
            ("1", "delusional", "Ken Carson", "https://i.scdn.co/image/ab67616d0000b273046eeb267309a2237cff41c7"),
            ("2", "Habits", "OsamaSon", "https://i.scdn.co/image/ab67616d0000b27341d8c624c257ffccbca8c3ad"),
            ("3", "I Rot, I Rot.", "Che", "https://i.scdn.co/image/ab67616d0000b2734b663f097a55ffafd8cab0e0"),
            ("4", "I Thought She Knew", "*NSYNC", "https://i.scdn.co/image/ab67616d0000b273a6cb8fab778e1efc406a5909"),
            ("5", "Studio Addict", "Nine Vicious", "https://i.scdn.co/image/ab67616d0000b273ec498907d4d654cf5dfd66cd")
        ]

        rows = []
        try:
            with sqlite3.connect("streamfolio.db") as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT track_id, track_name, artist_name, album_img, total_streams 
                    FROM streams GROUP BY track_id ORDER BY timestamp DESC LIMIT 5
                ''')
                rows = cursor.fetchall()
        except sqlite3.OperationalError:
            pass

        if not rows:
            print("[Notice] Database is empty. Injecting hardcoded visuals for UI testing...")
            rows = [(m[0], m[1], m[2], m[3], current_streams[m[1]]) for m in mock_ui_data]
            
        for row in rows:
            name = row[1]
            
            db_streams = row[4] if row[4] else 0
            streams = current_streams.get(name, db_streams)
            if streams == 0:
                streams = 1000000 
            
            gross = streams * 0.004 if streams >= 1000 else 0.0
            platform_fee = gross * 0.30
            net = gross - platform_fee

            portfolio.append({
                'track_id': row[0],
                'name': name,
                'artist': row[2],
                'album_img': row[3] if row[3] else "https://i.scdn.co/image/ab67616d0000b273046eeb267309a2237cff41c7",
                'est_streams': streams,
                'total_streams': streams,
                'gross': gross,
                'platform_fee': platform_fee,
                'net_royalty_pool': net,
                'finances': {'gross': gross, 'fee': platform_fee, 'net': net}
            })
            
        return portfolio