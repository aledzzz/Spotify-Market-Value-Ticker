import os
import requests
from dotenv import load_dotenv

load_dotenv()

def main():
    class LastFmPortfolio:
        def __init__(self):
            self.api_key = os.getenv('LASTFM_API_KEY')
            self.base_url = "http://ws.audioscrobbler.com/2.0/"
            # 2026 weighted averages
            self.payout_rate = 0.004 

        def get_top_5(self, username):
            """Fetches top 5 tracks and their album covers from Last.fm."""
            params = {
                'method': 'user.gettoptracks',
                'user': username,
                'api_key': self.api_key,
                'format': 'json',
                'limit': 5,
                'period': '12month' # Equivalent to the last year
            }
            
            response = requests.get(self.base_url, params=params).json()
            tracks = response.get('toptracks', {}).get('track', [])
            
            portfolio = []
            for t in tracks:
                # Last.fm provides images in a list of sizes; 
                # index 2 or 3 is typically the high-res 'large' or 'extralarge'
                img_url = t['image'][-1]['#text'] if t.get('image') else None
                
                portfolio.append({
                    "name": t['name'],
                    "artist": t['artist']['name'],
                    "album_img": img_url,
                    "playcount": int(t.get('playcount', 0))
                })
            return portfolio
