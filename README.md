# Streamfolio 

An end-to-end Fintech pipeline dashboard built to display a user's music portfolio based on their top 5 tracks and calculates the estimated gross/net revenue royalties using the 2026 music industry standards. Also focusing on real-time automation, this program vaults portfolio data into a local SQLite database and automatically generates CSV files for visualization in Tableau. 

# Prerequistes
- Python 3.11+
- Spotify API Developer Account (grab Spotify API key here: https://developer.spotify.com/)
- Tableau Desktop Liscense
- SQLite 3 Editor (IDE extension)
- pip install manager 

# Key Features
- Top 5 Tracks: Fetches a user's top 5 tracks over a 12-month period using Last.fm API
- Market Valuation: Calculates estimated revenue using the current industry baseline ($0.004 per stream & ~30% platform cut)
- Monetization Floor: Flags tracks that have reached 1,000 streams within a rolling 12-month period

# Setup
1.) Clone the repository
```
https://github.com/aledzzz/Streamfolio.git 
```
2.) Create a virtual environment
```
python -m venv venv
```
3.) Install dependencies
```
pip install -r requirements.txt
```
4.) Add your Spotify API keys to the .env file (redirect_url provided below)
```
client_id = "####"
client_secret = "####"
redirect_url = "http://127.0.0.1:8000/callback"
```
5.) Run
```
python main.py
```

